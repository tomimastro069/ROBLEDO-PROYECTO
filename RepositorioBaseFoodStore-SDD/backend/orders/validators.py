from .exceptions import InsufficientStockException
import asyncio
from decimal import Decimal
from .clients.inventory_client import InventoryClient
from .clients.catalog_client import CatalogClient
from .clients.payment_client import PaymentClient

def validate_product_availability(product_id: int, quantity: int) -> None:
    # Use real async inventory client
    client = InventoryClient(base_url="http://inventory:8001")
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    success = loop.run_until_complete(client.verify_and_deduct_stock(product_id, quantity))
    if not success:
        raise InsufficientStockException(f"Sin stock suficiente para el producto {product_id}")

def validate_price(product_id: int, price: Decimal) -> None:
    # Use catalog service for price validation
    client = CatalogClient(base_url="http://catalog:8002")
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    current = loop.run_until_complete(client.get_product_price(product_id))
    if Decimal(str(current)) != price:
        raise ValueError(f"El precio cambió para el producto {product_id}: esperado {price}, recibido {current}")

def validate_payment_method(order):
    # Example: expects order to have .id, .total, .payment_method
    client = PaymentClient(base_url="http://payment:8003")
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    authorized = loop.run_until_complete(client.authorize_payment(order.id, order.total, getattr(order, 'payment_method', "credit")))
    if not authorized:
        raise ValueError(f"Pago no autorizado para el pedido {order.id}")
