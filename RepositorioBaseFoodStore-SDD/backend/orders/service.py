from typing import List, Optional
import asyncio
from datetime import datetime
from sqlmodel import Session
from .models import Order, OrderItem, OrderStatus
from .repository import OrderRepository
from .exceptions import OrderNotFound
from .state_machine import OrderStateMachine
from .validators import validate_product_availability, validate_price, validate_payment_method
from .events import OrderCreated, OrderUpdated, OrderCancelled, OrderSubmitted
from .clients.event_publisher import EventPublisher

def publish_event(event):
    """
    Wrapper sincrónico para publicar eventos en RabbitMQ usando EventPublisher
    """
    event_type = event.__class__.__name__
    payload = event.dict()
    # RabbitMQ URL - idealmente de config/env
    publisher = EventPublisher(broker_url="amqp://guest:guest@rabbitmq:5672/")
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    if loop.is_running():
        # Si ya hay un loop corriendo (ej. en FastAPI), usamos ese
        asyncio.ensure_future(publisher.publish_event(event_type, payload))
    else:
        loop.run_until_complete(publisher.publish_event(event_type, payload))

import logging
import time
from .monitoring import ORDERS_CREATED, ORDER_DURATION, ORDER_ERRORS

class OrderService:
    def __init__(self, session: Session, correlation_id: Optional[str] = None):
        self.repo = OrderRepository(session)
        self.correlation_id = correlation_id
        self.logger = logging.getLogger("orders.service")

    def _log(self, level: int, msg: str):
        extra = {"correlation_id": self.correlation_id} if self.correlation_id else {}
        self.logger.log(level, msg, extra=extra)

    def create_order(self, user_id: int, items: List[dict], total: float) -> Order:
        start_time = time.time()
        self._log(logging.INFO, f"Creating order for user {user_id} with {len(items)} items. Total: {total}")
        
        try:
            # Phase 4 integration: Validaciones externas de Stock y Precio (Validators)
            for item in items:
                validate_product_availability(item["product_id"], item["quantity"])
                validate_price(item["product_id"], item["price"])
            
            # Persistencia inicial como DRAFT
            order = Order(user_id=user_id, status=OrderStatus.DRAFT, total=total)
            order_items = [OrderItem(**item) for item in items]
            order = self.repo.create(order, order_items)
            
            # Disparamos evento de creación
            ev_created = OrderCreated(
                order_id=order.id, 
                user_id=order.user_id, 
                items=[{"product_id": i.product_id, "quantity": i.quantity, "price": i.price} for i in order_items], 
                created_at=order.created_at
            )
            publish_event(ev_created)
            
            # Phase 4 integration: Autorización de Pago (requiere el ID del pedido persistido)
            validate_payment_method(order)
            
            # Transición a SUBMITTED una vez pagado exitosamente
            order = self.update_order(order.id, {"status": OrderStatus.SUBMITTED})
            
            # Track metrics
            ORDERS_CREATED.inc()
            ORDER_DURATION.observe((time.time() - start_time) * 1000)
            self._log(logging.INFO, f"Order {order.id} successfully submitted.")
            
            return order
            
        except Exception as e:
            ORDER_ERRORS.labels(type=type(e).__name__).inc()
            self._log(logging.ERROR, f"Order creation failed: {str(e)}")
            raise

    def get_order(self, order_id: int) -> Order:
        order = self.repo.get(order_id)
        if not order:
            raise OrderNotFound()
        return order

    def update_order(self, order_id: int, data: dict) -> Order:
        order = self.repo.get(order_id)
        if not order:
            raise OrderNotFound()
        
        from_status = order.status
        to_status = data.get("status", order.status)
        
        ev = None
        if from_status != to_status:
            OrderStateMachine.validate_transition(from_status, to_status)
            order.status = to_status
            
            # Phase 4 integration: Publicación de eventos específicos por cambio de estado
            if to_status == OrderStatus.SUBMITTED:
                ev = OrderSubmitted(order_id=order.id, user_id=order.user_id, submitted_at=datetime.utcnow())
            elif to_status == OrderStatus.CANCELLED:
                ev = OrderCancelled(order_id=order.id, user_id=order.user_id, cancelled_at=datetime.utcnow())

        # Si no hubo evento específico, mandamos un OrderUpdated genérico
        if not ev:
            ev = OrderUpdated(order_id=order.id, user_id=order.user_id, updated_at=datetime.utcnow())

        # Actualizar en el repositorio
        order = self.repo.update(order, **data)
        
        # Publicación del evento integrado en el flujo
        publish_event(ev)
        
        return order

    def cancel_order(self, order_id: int) -> None:
        # Centralizamos la lógica de cancelación a través de update_order
        self.update_order(order_id, {"status": OrderStatus.CANCELLED})

    def list_orders(self, user_id: int, skip: int = 0, limit: int = 20) -> List[Order]:
        return self.repo.list_by_user(user_id, skip, limit)

