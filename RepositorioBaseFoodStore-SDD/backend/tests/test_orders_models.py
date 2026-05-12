import pytest
from orders.models import Order, OrderItem, OrderStatus
from datetime import datetime

def test_order_model_creation():
    order = Order(
        user_id=1,
        status=OrderStatus.DRAFT,
        total=100.0
    )
    assert order.user_id == 1
    assert order.status == OrderStatus.DRAFT
    assert order.total == 100.0
    assert isinstance(order.created_at, datetime)

def test_order_item_model_creation():
    item = OrderItem(
        order_id=1,
        product_id=10,
        quantity=2,
        price=50.0
    )
    assert item.order_id == 1
    assert item.product_id == 10
    assert item.quantity == 2
    assert item.price == 50.0

def test_order_status_enum():
    assert OrderStatus.DRAFT == "draft"
    assert OrderStatus.SUBMITTED == "submitted"
    assert OrderStatus.PROCESSING == "processing"
    assert OrderStatus.COMPLETED == "completed"
    assert OrderStatus.CANCELLED == "cancelled"
