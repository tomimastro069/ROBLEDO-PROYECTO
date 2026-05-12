import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from datetime import datetime
from decimal import Decimal

from main import app
from app.core.database import get_session
from auth.dependencies import get_current_user
from auth.schemas import TokenData
from auth.roles import Role
from orders.models import OrderStatus
from orders.exceptions import OrderNotFoundException, InvalidStateTransitionException

@pytest.fixture(name="client")
def client_fixture():
    # En TDD puro, mockeamos la DB para testear solo la lógica del Router
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture
def customer_user():
    return TokenData(sub="1", role=Role.CLIENT, email="customer@test.com")

@pytest.fixture
def admin_user():
    return TokenData(sub="2", role=Role.ADMIN, email="admin@test.com")

@patch("orders.routes.OrderService")
def test_create_order_api_success(mock_service_class, client, customer_user):
    app.dependency_overrides[get_current_user] = lambda: customer_user
    
    mock_service = mock_service_class.return_value
    mock_order = MagicMock()
    mock_order.id = 100
    mock_order.user_id = 1
    mock_order.status = "PENDIENTE"
    mock_order.total = Decimal("1500.50")
    mock_order.items = []
    mock_order.direccion_calle = "Falsa"
    mock_order.direccion_numero = "123"
    mock_order.direccion_ciudad = "CABA"
    mock_order.created_at = datetime.utcnow()
    mock_order.updated_at = datetime.utcnow()
    
    mock_service.create_order.return_value = mock_order
    
    payload = {
        "items": [{"product_id": 1, "quantity": 2, "exclusions": [10]}],
        "shipping_address_id": 5
    }
    
    response = client.post("/api/v1/orders/orders", json=payload)
    
    assert response.status_code == 201
    assert response.json()["id"] == 100
    assert response.json()["status"] == "PENDIENTE"

@patch("orders.routes.OrderService")
def test_cancel_order_unauthorized(mock_service_class, client, customer_user):
    app.dependency_overrides[get_current_user] = lambda: customer_user
    
    mock_service = mock_service_class.return_value
    mock_order = MagicMock()
    mock_order.user_id = 999  # No es el dueño
    mock_service.get_order.return_value = mock_order
    
    response = client.patch("/api/v1/orders/orders/100/cancel", json={"reason": "Test"})
    
    assert response.status_code == 403

@patch("orders.routes.OrderService")
def test_cancel_order_fsm_violation(mock_service_class, client, customer_user):
    app.dependency_overrides[get_current_user] = lambda: customer_user
    
    mock_service = mock_service_class.return_value
    mock_order = MagicMock()
    mock_order.user_id = 1
    mock_service.get_order.return_value = mock_order
    
    # Mockeamos que el service lance la excepción de FSM
    mock_service.cancel_order.side_effect = InvalidStateTransitionException("No se puede cancelar en este estado")
    
    response = client.patch("/api/v1/orders/orders/100/cancel", json={"reason": "Test"})
    
    assert response.status_code == 400
    assert "No se puede cancelar" in response.json()["detail"]

@patch("orders.routes.OrderService")
def test_admin_list_orders(mock_service_class, client, admin_user):
    app.dependency_overrides[get_current_user] = lambda: admin_user
    
    mock_service = mock_service_class.return_value
    mock_service.repo.list_all.return_value = []
    
    response = client.get("/api/v1/orders/admin/orders")
    
    assert response.status_code == 200
    mock_service.repo.list_all.assert_called()

@patch("orders.routes.OrderService")
def test_get_order_detail_success(mock_service_class, client, customer_user):
    app.dependency_overrides[get_current_user] = lambda: customer_user
    
    mock_service = mock_service_class.return_value
    mock_order = MagicMock()
    mock_order.id = 100
    mock_order.user_id = 1 # Coincide con customer_user.sub
    mock_order.status = "PENDIENTE"
    mock_order.total = Decimal("100.00")
    mock_order.items = []
    mock_order.direccion_calle = "X"
    mock_order.direccion_numero = "1"
    mock_order.direccion_ciudad = "Y"
    
    mock_service.get_order.return_value = mock_order
    
    response = client.get("/api/v1/orders/orders/100")
    
    assert response.status_code == 200
    assert response.json()["id"] == 100

@patch("orders.routes.OrderService")
def test_admin_update_status_success(mock_service_class, client, admin_user):
    app.dependency_overrides[get_current_user] = lambda: admin_user
    
    mock_service = mock_service_class.return_value
    mock_order = MagicMock()
    mock_order.status = "CONFIRMADO"
    mock_service.update_order.return_value = mock_order
    
    payload = {"new_status": "CONFIRMADO", "reason": "Pago verificado"}
    response = client.patch("/api/v1/orders/admin/orders/100/status", json=payload)
    
    assert response.status_code == 200
    assert response.json()["status"] == "CONFIRMADO"
    mock_service.update_order.assert_called_with(100, {"status": "CONFIRMADO"})
