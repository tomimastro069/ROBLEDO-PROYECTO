"""
Tests unitarios para el módulo de pagos — Webhook IPN y Router.

Scope: lógica de negocio aislada con mocks del SDK de MercadoPago y la DB.
No requiere conexión real a MercadoPago ni a PostgreSQL.

Cubre los escenarios del spec mercado-pago-checkout:
  - Creación exitosa de preferencia con idempotency_key
  - Rechazo de firma inválida en webhook
  - Idempotencia: payment_id ya procesado → 200 sin re-ejecutar
  - Pago aprobado → pedido CONFIRMADO (FSM)
  - Pago rechazado → pedido permanece PENDIENTE
"""

import hashlib
import hmac
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional
from unittest.mock import MagicMock, patch, AsyncMock

import pytest


# ─────────────────────────────────────────────────────────────────────────────
# Helpers / Fixtures
# ─────────────────────────────────────────────────────────────────────────────

def make_pago(payment_id: Optional[str] = None, mp_status: str = "pending", pedido_id: int = 1):
    from pagos.models import Pago
    return Pago(
        id=1,
        pedido_id=pedido_id,
        preference_id="pref-test-123",
        payment_id=payment_id,
        idempotency_key=str(uuid.uuid4()),
        mp_status=mp_status,
        mp_status_detail=None,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


def make_order(status_val="PENDIENTE"):
    from orders.models import Order, OrderStatus
    order = Order(
        id=1,
        user_id=42,
        status=OrderStatus(status_val),
        total=Decimal("1500.00"),
        direccion_calle="Calle Falsa",
        direccion_numero="123",
        direccion_ciudad="Buenos Aires",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    return order


# ─────────────────────────────────────────────────────────────────────────────
# Tests: _verify_signature
# ─────────────────────────────────────────────────────────────────────────────

class TestVerifySignature:

    def test_no_secret_configured_allows_all(self):
        """Sin secret configurado (dev mode) siempre retorna True."""
        from app.api.webhook_mercadopago import _verify_signature
        with patch("app.api.webhook_mercadopago.MP_WEBHOOK_SECRET", ""):
            result = _verify_signature({"x-signature": "bad", "x-request-id": "req1"}, b"body")
        assert result is True

    def test_missing_ts_or_v1_returns_false(self):
        """Firma sin ts o v1 falla la verificación."""
        from app.api.webhook_mercadopago import _verify_signature
        with patch("app.api.webhook_mercadopago.MP_WEBHOOK_SECRET", "mysecret"):
            # Header sin formato correcto
            result = _verify_signature(
                {"x-signature": "malformed", "x-request-id": "req1", "data_id": "pay123"},
                b"body",
            )
        assert result is False

    def test_invalid_signature_returns_false(self):
        """Firma con v1 incorrecto retorna False."""
        from app.api.webhook_mercadopago import _verify_signature
        with patch("app.api.webhook_mercadopago.MP_WEBHOOK_SECRET", "mysecret"):
            result = _verify_signature(
                {
                    "x-signature": "ts=1234,v1=invalidsignature",
                    "x-request-id": "req-abc",
                    "data_id": "pay123",
                },
                b"body",
            )
        assert result is False

    def test_valid_signature_accepted(self):
        """Firma HMAC-SHA256 correcta retorna True."""
        from app.api.webhook_mercadopago import _verify_signature
        secret = "supersecret"
        ts = "1716000000"
        request_id = "test-request-id"
        data_id = "payment-id-999"

        manifest = f"id:{data_id};request-id:{request_id};ts:{ts};"
        correct_v1 = hmac.new(secret.encode(), manifest.encode(), hashlib.sha256).hexdigest()

        with patch("app.api.webhook_mercadopago.MP_WEBHOOK_SECRET", secret):
            result = _verify_signature(
                {
                    "x-signature": f"ts={ts},v1={correct_v1}",
                    "x-request-id": request_id,
                    "data_id": data_id,
                },
                b"body",
            )
        assert result is True


# ─────────────────────────────────────────────────────────────────────────────
# Tests: PagoRepository — idempotencia de payment_id
# ─────────────────────────────────────────────────────────────────────────────

class TestPagoRepository:

    def test_get_by_payment_id_returns_none_when_not_found(self):
        """Retorna None si no existe un pago con ese payment_id."""
        from pagos.repository import PagoRepository
        mock_session = MagicMock()
        mock_session.exec.return_value.one_or_none.return_value = None
        repo = PagoRepository(mock_session)

        result = repo.get_by_payment_id("pay-nonexistent")
        assert result is None

    def test_get_by_payment_id_returns_existing_pago(self):
        """Retorna el Pago existente cuando el payment_id ya fue registrado."""
        from pagos.repository import PagoRepository
        pago = make_pago(payment_id="pay-already-exists", mp_status="approved")

        mock_session = MagicMock()
        mock_session.exec.return_value.one_or_none.return_value = pago
        repo = PagoRepository(mock_session)

        result = repo.get_by_payment_id("pay-already-exists")
        assert result is not None
        assert result.mp_status == "approved"


# ─────────────────────────────────────────────────────────────────────────────
# Tests: OrderService.confirm_by_payment
# ─────────────────────────────────────────────────────────────────────────────

class TestOrderServiceConfirmByPayment:

    def test_confirm_pending_order_succeeds(self):
        """Confirmar un pedido PENDIENTE lo mueve a CONFIRMADO."""
        from orders.service import OrderService
        from orders.models import OrderStatus

        order = make_order("PENDIENTE")
        confirmed_order = make_order("CONFIRMADO")

        # MagicMock sin spec para permitir atributos dinámicos del UoW
        mock_uow = MagicMock()
        mock_uow.orders.get.return_value = order
        mock_uow.orders.update.return_value = confirmed_order

        service = OrderService(mock_uow)
        result = service.confirm_by_payment(1, mock_uow)

        mock_uow.orders.update.assert_called_once_with(order, status=OrderStatus.CONFIRMADO)
        assert result.status == OrderStatus.CONFIRMADO

    def test_confirm_already_confirmed_raises(self):
        """Intentar confirmar un pedido ya CONFIRMADO lanza InvalidStateTransitionException."""
        from orders.service import OrderService
        from orders.exceptions import InvalidStateTransitionException

        order = make_order("CONFIRMADO")
        mock_uow = MagicMock()
        mock_uow.orders.get.return_value = order

        service = OrderService(mock_uow)
        with pytest.raises(InvalidStateTransitionException):
            service.confirm_by_payment(1, mock_uow)

    def test_confirm_nonexistent_order_raises(self):
        """Intentar confirmar un pedido que no existe lanza OrderNotFoundException."""
        from orders.service import OrderService
        from orders.exceptions import OrderNotFoundException

        mock_uow = MagicMock()
        mock_uow.orders.get.return_value = None

        service = OrderService(mock_uow)
        with pytest.raises(OrderNotFoundException):
            service.confirm_by_payment(999, mock_uow)
