import pytest
import threading
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from unittest.mock import patch, AsyncMock
from orders.service import OrderService

@pytest.fixture(name="session")
def session_fixture():
    # SQLite in-memory with StaticPool allows sharing the same connection across threads for testing
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@patch("orders.validators.InventoryClient")
@patch("orders.validators.CatalogClient")
@patch("orders.validators.PaymentClient")
@patch("orders.service.publish_event")
def test_concurrent_order_submissions(mock_publish, mock_pay, mock_cat, mock_inv, session):
    """
    Stress test with 10+ simultaneous order creation requests
    """
    # Setup mocks for external services
    mock_inv.return_value.verify_and_deduct_stock = AsyncMock(return_value=True)
    mock_cat.return_value.get_product_price = AsyncMock(return_value=10.0)
    mock_pay.return_value.authorize_payment = AsyncMock(return_value=True)

    service = OrderService(session)
    num_threads = 12
    orders = []
    errors = []

    def create_order_task(idx):
        try:
            # Using unique user_id to simulate different users
            order = service.create_order(user_id=idx, items=[{"product_id": 1, "quantity": 1, "price": 10.0}], total=10.0)
            orders.append(order)
        except Exception as e:
            errors.append(e)

    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=create_order_task, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Verify no crashes occurred during concurrent access
    assert len(errors) == 0, f"Errors occurred during concurrency test: {errors}"
    assert len(orders) == num_threads
    
    # Verify all orders were persisted correctly
    for order in orders:
        assert order.id is not None
        assert order.status == "submitted"
