import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from orders.validators import validate_product_availability, validate_price, validate_payment_method
from orders.exceptions import InsufficientStock

@patch("orders.validators.InventoryClient")
def test_validate_product_availability_success(mock_client_class):
    mock_client = mock_client_class.return_value
    mock_client.verify_and_deduct_stock = AsyncMock(return_value=True)
    
    # Should not raise
    validate_product_availability(1, 5)
    # Note: the mock is called within the loop, so we check if the async method was called
    mock_client.verify_and_deduct_stock.assert_called_with(1, 5)

@patch("orders.validators.InventoryClient")
def test_validate_product_availability_insufficient(mock_client_class):
    mock_client = mock_client_class.return_value
    mock_client.verify_and_deduct_stock = AsyncMock(return_value=False)
    
    with pytest.raises(InsufficientStock):
        validate_product_availability(1, 5)

@patch("orders.validators.CatalogClient")
def test_validate_price_success(mock_client_class):
    mock_client = mock_client_class.return_value
    mock_client.get_product_price = AsyncMock(return_value=10.0)
    
    validate_price(1, 10.0)

@patch("orders.validators.CatalogClient")
def test_validate_price_mismatch(mock_client_class):
    mock_client = mock_client_class.return_value
    mock_client.get_product_price = AsyncMock(return_value=12.0)
    
    with pytest.raises(ValueError, match="Price changed"):
        validate_price(1, 10.0)

@patch("orders.validators.PaymentClient")
def test_validate_payment_method_success(mock_client_class):
    mock_client = mock_client_class.return_value
    mock_client.authorize_payment = AsyncMock(return_value=True)
    
    order = MagicMock(id=1, total=100.0)
    validate_payment_method(order)

@patch("orders.validators.PaymentClient")
def test_validate_payment_method_failed(mock_client_class):
    mock_client = mock_client_class.return_value
    mock_client.authorize_payment = AsyncMock(return_value=False)
    
    order = MagicMock(id=1, total=100.0)
    with pytest.raises(ValueError, match="Payment not authorized"):
        validate_payment_method(order)
