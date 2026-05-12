import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from unittest.mock import MagicMock, patch

from main import app
from app.core.database import get_session
from auth.dependencies import get_current_user
from auth.schemas import TokenData
from auth.roles import Role
from orders.models import OrderStatus

# Setup engine/session
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture
def mock_user():
    return TokenData(sub="1", role=Role.CLIENTE, email="test@test.com")

@pytest.fixture
def admin_user():
    return TokenData(sub="2", role=Role.ADMIN, email="admin@test.com")

@patch("orders.routes.OrderService")
def test_create_order_route(mock_service_class, client, mock_user):
    app.dependency_overrides[get_current_user] = lambda: mock_user
    
    mock_service = mock_service_class.return_value
    # Use a real object that has from_orm capability if needed, or mock carefully
    # OrderResponse.from_orm(order) expects an object with attributes matching the schema
    mock_order = MagicMock()
    mock_order.id = 1
    mock_order.user_id = 1
    mock_order.status = OrderStatus.DRAFT
    mock_order.total = 100.0
    mock_order.items = []
    mock_order.created_at = "2024-01-01T00:00:00"
    
    mock_service.create_order.return_value = mock_order
    
    payload = {
        "items": [{"product_id": 1, "quantity": 1, "price": 100.0}],
        "total": 100.0
    }
    
    response = client.post("/api/v1/orders/orders", json=payload)
    
    # We might need to mock from_orm in the response model too if it fails
    assert response.status_code == 201
    mock_service.create_order.assert_called()

@patch("orders.routes.OrderService")
def test_get_order_route_forbidden(mock_service_class, client, mock_user):
    app.dependency_overrides[get_current_user] = lambda: mock_user
    
    mock_service = mock_service_class.return_value
    mock_order = MagicMock()
    mock_order.user_id = 999  # Not the current user
    mock_service.get_order.return_value = mock_order
    
    response = client.get("/api/v1/orders/orders/1")
    
    assert response.status_code == 403

@patch("orders.routes.OrderService")
def test_get_order_route_as_admin(mock_service_class, client, admin_user):
    app.dependency_overrides[get_current_user] = lambda: admin_user
    
    mock_service = mock_service_class.return_value
    mock_order = MagicMock()
    mock_order.user_id = 1
    mock_order.id = 123
    mock_order.status = OrderStatus.DRAFT
    mock_order.total = 50.0
    mock_order.items = []
    mock_order.created_at = "2024-01-01T00:00:00"
    
    mock_service.get_order.return_value = mock_order
    
    response = client.get("/api/v1/orders/orders/123")
    
    assert response.status_code == 200
    assert response.json()["id"] == 123
