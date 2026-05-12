from enum import Enum
from .models import OrderStatus
from .exceptions import InvalidStateTransitionException

class OrderStateMachine:
    allowed_transitions = {
        OrderStatus.PENDIENTE: {OrderStatus.CONFIRMADO, OrderStatus.CANCELADO},
        OrderStatus.CONFIRMADO: {OrderStatus.EN_PREPARACION, OrderStatus.CANCELADO},
        OrderStatus.EN_PREPARACION: {OrderStatus.EN_CAMINO, OrderStatus.CANCELADO},
        OrderStatus.EN_CAMINO: {OrderStatus.ENTREGADO},
        OrderStatus.ENTREGADO: set(),
        OrderStatus.CANCELADO: set(),
    }

    @classmethod
    def validate_transition(cls, from_status: OrderStatus, to_status: OrderStatus):
        if to_status not in cls.allowed_transitions.get(from_status, set()):
            raise InvalidStateTransitionException(f"Transición inválida: {from_status} -> {to_status}")
