from typing import List, Optional
import asyncio
from datetime import datetime
from decimal import Decimal
from .models import Order, OrderItem, OrderStatus
from .repository import OrderRepository
from .exceptions import OrderNotFoundException, InvalidStateTransitionException
from .state_machine import OrderStateMachine
from .events import OrderCreated, OrderUpdated, OrderCancelled, OrderSubmitted
from .clients.event_publisher import EventPublisher
from app.core.uow.unit_of_work import AppUnitOfWork

import logging
import time

def publish_event(event):
    """
    Wrapper sincrónico para publicar eventos (simplificado para evitar bloqueos si RabbitMQ no está)
    """
    try:
        event_type = event.__class__.__name__
        payload = event.dict()
        # En este entorno de desarrollo, si RabbitMQ falla, solo lo logueamos
        publisher = EventPublisher(broker_url="amqp://guest:guest@rabbitmq:5672/")
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.ensure_future(publisher.publish_event(event_type, payload))
        else:
            loop.run_until_complete(publisher.publish_event(event_type, payload))
    except Exception as e:
        logging.getLogger("orders.events").warning(f"Could not publish event: {e}")

class OrderService:
    def __init__(self, uow: AppUnitOfWork, correlation_id: Optional[str] = None):
        self.uow = uow
        self.correlation_id = correlation_id
        self.logger = logging.getLogger("orders.service")

    def _log(self, level: int, msg: str):
        extra = {"correlation_id": self.correlation_id} if self.correlation_id else {}
        self.logger.log(level, msg, extra=extra)

    def create_order(self, user_id: int, shipping_address_id: int, items: List[dict]) -> Order:
        start_time = time.time()
        self._log(logging.INFO, f"Creating order for user {user_id} with address {shipping_address_id}")
        
        with self.uow as uow:
            # 1. Validar y obtener dirección (Snapshot)
            address = uow.addresses.get_by_id(shipping_address_id)
            if not address or address.user_id != user_id:
                raise ValueError("Dirección no válida o no pertenece al usuario")

            # 2. Procesar ítems y buscar precios reales
            total = Decimal("0.00")
            order_items = []
            
            for item_data in items:
                product = uow.products.get_by_id(item_data["product_id"])
                if not product:
                    raise ValueError(f"Producto {item_data['product_id']} no encontrado")
                
                if product.stock < item_data["quantity"]:
                    raise ValueError(f"Stock insuficiente para el producto {product.name}")
                
                # Descontar stock
                product.stock -= item_data["quantity"]
                uow.products.update(product)
                
                price_snapshot = product.price
                item_total = price_snapshot * item_data["quantity"]
                total += item_total
                
                order_items.append(OrderItem(
                    product_id=product.id,
                    quantity=item_data["quantity"],
                    price_snapshot=price_snapshot,
                    exclusions=item_data.get("exclusions", [])
                ))

            # 3. Crear el pedido con snapshots
            order = Order(
                user_id=user_id,
                status=OrderStatus.PENDIENTE,
                total=total,
                direccion_calle=address.street,
                direccion_numero=address.numero,
                direccion_ciudad=address.city
            )
            
            # Persistencia a través del repositorio de órdenes (que ya está en el UOW)
            order = uow.orders.create(order, order_items)
            
            # 4. Disparar evento de creación
            ev_created = OrderCreated(
                order_id=order.id, 
                user_id=order.user_id, 
                items=[{
                    "product_id": i.product_id, 
                    "quantity": i.quantity, 
                    "price": str(i.price_snapshot)
                } for i in order_items], 
                created_at=order.created_at
            )
            publish_event(ev_created)
            
            self._log(logging.INFO, f"Order {order.id} successfully created via UOW.")
            return order

    def get_order(self, order_id: int) -> Order:
        with self.uow as uow:
            order = uow.orders.get(order_id)
            if not order:
                raise OrderNotFoundException()
            return order

    def update_order(self, order_id: int, data: dict) -> Order:
        with self.uow as uow:
            order = uow.orders.get(order_id)
            if not order:
                raise OrderNotFoundException()
            
            from_status = order.status
            to_status = data.get("status", order.status)
            
            if from_status != to_status:
                OrderStateMachine.validate_transition(from_status, to_status)
                
            order = uow.orders.update(order, **data)
            return order

    def list_orders(self, user_id: Optional[int] = None, skip: int = 0, limit: int = 20) -> List[Order]:
        with self.uow as uow:
            if user_id:
                return uow.orders.list_by_user(user_id, skip, limit)
            return uow.orders.list_all(skip, limit)

    def cancel_order(self, order_id: int, reason: str = "No reason provided") -> None:
        self.update_order(order_id, {"status": OrderStatus.CANCELADO})
