import pytest
from unittest.mock import MagicMock, patch
from orders.service import OrderService
from orders.models import OrderStatus
from orders.exceptions import OrderNotFound

@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def service(mock_session):
    return OrderService(mock_session)

def test_get_order_success(service):
    mock_order = MagicMock()
    service.repo.get = MagicMock(return_value=mock_order)
    
    result = service.get_order(1)
    assert result == mock_order
    service.repo.get.assert_called_with(1)

def test_get_order_not_found(service):
    service.repo.get = MagicMock(return_value=None)
    with pytest.raises(OrderNotFound):
        service.get_order(999)

@patch("orders.service.validate_product_availability")
@patch("orders.service.validate_price")
@patch("orders.service.validate_payment_method")
@patch("orders.service.publish_event")
def test_create_order_flow(mock_publish, mock_pay, mock_price, mock_avail, service):
    user_id = 1
    items = [{"product_id": 1, "quantity": 2, "price": 10.0}]
    total = 20.0
    
    # Mocking order and items
    mock_order = MagicMock(id=123, user_id=user_id, status=OrderStatus.DRAFT, total=total)
    mock_order.created_at = "now"
    
    service.repo.create = MagicMock(return_value=mock_order)
    service.repo.get = MagicMock(return_value=mock_order)
    service.repo.update = MagicMock(return_value=mock_order)
    
    result = service.create_order(user_id, items, total)
    
    assert result == mock_order
    mock_avail.assert_called()
    mock_price.assert_called()
    mock_pay.assert_called_with(mock_order)
    # Check if update was called to SUBMITTED
    service.repo.update.assert_called()
    args, kwargs = service.repo.update.call_args
    assert kwargs["status"] == OrderStatus.SUBMITTED

@patch("orders.service.publish_event")
def test_cancel_order(mock_publish, service):
    mock_order = MagicMock(id=123, status=OrderStatus.SUBMITTED, user_id=1)
    service.repo.get = MagicMock(return_value=mock_order)
    service.repo.update = MagicMock(return_value=mock_order)
    
    service.cancel_order(123)
    
    service.repo.update.assert_called()
    args, kwargs = service.repo.update.call_args
    assert kwargs["status"] == OrderStatus.CANCELLED

def test_list_orders(service):
    mock_orders = [MagicMock(), MagicMock()]
    service.repo.list_by_user = MagicMock(return_value=mock_orders)
    
    result = service.list_orders(user_id=1)
    assert result == mock_orders
    service.repo.list_by_user.assert_called_with(1, 0, 20)
