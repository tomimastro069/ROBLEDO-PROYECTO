from .exceptions import InsufficientStock

# These call real clients for external orchestrations

import asyncio
from .clients.inventory_client import InventoryClient
from .exceptions import InsufficientStock

def validate_product_availability(product_id: int, quantity: int) -> None:
    # Use real async inventory client
    client = InventoryClient(base_url="http://inventory:8001")
    loop = asyncio.get_event_loop()
    success = loop.run_until_complete(client.verify_and_deduct_stock(product_id, quantity))
    if not success:
        raise InsufficientStock(f"Not enough stock for product {product_id}")

from .clients.catalog_client import CatalogClient

def validate_price(product_id: int, price: float) -> None:
    # Use catalog service for price validation
    client = CatalogClient(base_url="http://catalog:8002")
    loop = asyncio.get_event_loop()
    current = loop.run_until_complete(client.get_product_price(product_id))
    if current != price:
        raise ValueError(f"Price changed for product {product_id}: expected {price}, got {current}")

from .clients.payment_client import PaymentClient

def validate_payment_method(order):
    # Example: expects order to have .id, .total, .payment_method
    client = PaymentClient(base_url="http://payment:8003")
    loop = asyncio.get_event_loop()
    authorized = loop.run_until_complete(client.authorize_payment(order.id, order.total, getattr(order, 'payment_method', "credit")))
    if not authorized:
        raise ValueError(f"Payment not authorized for order {order.id}")
