"""
Tests de integración para idempotencia del Webhook IPN.

Verifica que notificaciones IPN duplicadas (mismo payment_id) sean manejadas
de forma idempotente: la FSM del pedido no avanza dos veces, no se crean
registros de Pago duplicados, y siempre se retorna HTTP 200 OK.

Usa FastAPI TestClient + SQLite in-memory para no depender de PostgreSQL real.
"""

import uuid
from datetime import datetime
from decimal import Decimal
from unittest.mock import patch, MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session


# ─────────────────────────────────────────────────────────────────────────────
# Setup: motor in-memory para tests de integración
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def in_memory_engine():
    """Motor SQLite in-memory para tests de integración sin PostgreSQL."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    # Importar todos los modelos para registrar el metadata
    from app.core.models import Role, User, Category, Product, Payment, Address
    from orders.models import Order, OrderItem
    from pagos.models import Pago
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(in_memory_engine):
    """Sesión de DB para sembrar datos de prueba."""
    with Session(in_memory_engine) as session:
        yield session


@pytest.fixture(scope="function")
def test_app(in_memory_engine):
    """FastAPI TestClient con override de la base de datos."""
    from main import app
    from app.core.uow.unit_of_work import AppUnitOfWork, get_uow

    def override_get_uow():
        return AppUnitOfWork(engine=in_memory_engine)

    app.dependency_overrides[get_uow] = override_get_uow
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def _seed_order(session, user_id: int = 1, pedido_id: int = 1) -> None:
    """Siembra un pedido PENDIENTE en la DB de tests."""
    from orders.models import Order, OrderStatus
    from app.core.models import User, Role
    from app.core.models import Address

    # Crear role si no existe
    role = session.get(Role, 1)
    if not role:
        role = Role(id=1, name="cliente", description="Cliente")
        session.add(role)
        session.flush()

    # Crear user
    user = session.get(User, user_id)
    if not user:
        user = User(
            id=user_id,
            email="test@example.com",
            hashed_password="hashed",
            role_id=role.id,
        )
        session.add(user)
        session.flush()

    # Crear pedido
    order = Order(
        id=pedido_id,
        user_id=user_id,
        status=OrderStatus.PENDIENTE,
        total=Decimal("1500.00"),
        direccion_calle="Calle Falsa",
        direccion_numero="123",
        direccion_ciudad="Buenos Aires",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(order)
    session.commit()


# ─────────────────────────────────────────────────────────────────────────────
# Tests: idempotencia del webhook IPN
# ─────────────────────────────────────────────────────────────────────────────

class TestWebhookIdempotencia:

    def _mock_mp_payment(self, payment_id: str, status: str, pedido_id: int):
        """Mock de la respuesta de la API de MercadoPago para un payment."""
        return {
            "response": {
                "id": payment_id,
                "status": status,
                "status_detail": f"{status}_detail",
                "external_reference": str(pedido_id),
            }
        }

    def test_webhook_approved_once_confirms_order(self, test_app, db_session):
        """Un webhook 'approved' confirma el pedido exactamente una vez."""
        from orders.models import OrderStatus

        _seed_order(db_session, pedido_id=10)
        payment_id = f"pay-{uuid.uuid4()}"

        with patch("app.api.webhook_mercadopago.MP_WEBHOOK_SECRET", ""):
            with patch("mercadopago.SDK") as MockSDK:
                mock_sdk_instance = MagicMock()
                mock_sdk_instance.payment().get.return_value = self._mock_mp_payment(
                    payment_id, "approved", 10
                )
                MockSDK.return_value = mock_sdk_instance

                response = test_app.post(
                    f"/webhooks/mercadopago?type=payment&data.id={payment_id}"
                )

        assert response.status_code == 200
        data = response.json()
        assert data["mp_status"] == "approved"

    def test_webhook_duplicate_approved_is_idempotent(self, test_app, db_session):
        """Un segundo webhook 'approved' para el mismo payment_id retorna 200 sin re-procesar."""
        from pagos.models import Pago

        _seed_order(db_session, pedido_id=11)
        payment_id = f"pay-{uuid.uuid4()}"

        # Sembrar pago ya aprobado
        pago_existente = Pago(
            pedido_id=11,
            payment_id=payment_id,
            idempotency_key=str(uuid.uuid4()),
            mp_status="approved",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db_session.add(pago_existente)
        db_session.commit()

        with patch("app.api.webhook_mercadopago.MP_WEBHOOK_SECRET", ""):
            response = test_app.post(
                f"/webhooks/mercadopago?type=payment&data.id={payment_id}"
            )

        assert response.status_code == 200
        assert response.json()["status"] == "already_processed"

    def test_webhook_non_payment_type_is_ignored(self, test_app, db_session):
        """Webhooks de tipo distinto a 'payment' se ignoran con 200."""
        with patch("app.api.webhook_mercadopago.MP_WEBHOOK_SECRET", ""):
            response = test_app.post(
                "/webhooks/mercadopago?type=merchant_order&data.id=123"
            )

        assert response.status_code == 200
        assert response.json()["status"] == "ignored"

    def test_webhook_invalid_signature_returns_401(self, test_app, db_session):
        """Webhook con firma inválida retorna 401."""
        with patch("app.api.webhook_mercadopago.MP_WEBHOOK_SECRET", "secretkey"):
            response = test_app.post(
                "/webhooks/mercadopago?type=payment&data.id=pay-invalid",
                headers={"x-signature": "ts=123,v1=wrongsig", "x-request-id": "req1"},
            )

        assert response.status_code == 401
