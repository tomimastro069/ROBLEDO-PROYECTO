from enum import Enum
from .models import OrderStatus
from .exceptions import InvalidStatusTransition

class OrderStateMachine:
    allowed_transitions = {
        OrderStatus.DRAFT: {OrderStatus.SUBMITTED},
        OrderStatus.SUBMITTED: {OrderStatus.PROCESSING, OrderStatus.CANCELLED},
        OrderStatus.PROCESSING: {OrderStatus.COMPLETED, OrderStatus.CANCELLED},
        OrderStatus.COMPLETED: set(),
        OrderStatus.CANCELLED: set(),
    }

    @classmethod
    def validate_transition(cls, from_status: OrderStatus, to_status: OrderStatus):
        if to_status not in cls.allowed_transitions[from_status]:
            raise InvalidStatusTransition(f"Invalid transition: {from_status} -> {to_status}")
