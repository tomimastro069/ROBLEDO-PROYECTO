import pytest
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from unittest.mock import patch, AsyncMock
from orders.service import OrderService
from orders.models import OrderStatus

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@patch("orders.validators.InventoryClient")
@patch("orders.validators.CatalogClient")
@patch("orders.validators.PaymentClient")
@patch("orders.service.publish_event")
def test_full_order_flow_integration(mock_publish, mock_pay_class, mock_cat_class, mock_inv_class, session):
    """
    Test flow: create_order -> validators (inv, cat) -> persist (draft) -> event (created) -> payment -> transition (submitted) -> event (submitted)
    """
    # Setup mocks for external services
    mock_inv = mock_inv_class.return_value
    mock_inv.verify_and_deduct_stock = AsyncMock(return_value=True)
    
    mock_cat = mock_cat_class.return_value
    mock_cat.get_product_price = AsyncMock(return_value=10.0)
    
    mock_pay = mock_pay_class.return_value
    mock_pay.authorize_payment = AsyncMock(return_value=True)
    
    service = OrderService(session)
    user_id = 1
    items = [{"product_id": 1, "quantity": 2, "price": 10.0}]
    total = 20.0
    
    # Execute
    order = service.create_order(user_id, items, total)
    
    # Assertions
    assert order.id is not None
    assert order.status == OrderStatus.SUBMITTED
    assert order.total == 20.0
    assert len(order.items) == 1
    assert order.items[0].product_id == 1
    
    # Verify that events were published
    # 1. OrderCreated
    # 2. OrderSubmitted (inside update_order)
    assert mock_publish.call_count >= 2
    
    # Verify specific event types if possible
    calls = mock_publish.call_args_list
    event_names = [call.args[0].__class__.__name__ for call in calls]
    assert "OrderCreated" in event_names
    assert "OrderSubmitted" in event_names
