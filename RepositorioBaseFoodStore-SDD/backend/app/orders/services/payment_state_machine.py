from enum import Enum, auto
from typing import Optional

class PaymentState(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class PaymentStateMachine:
    """
    Encapsulates payment/order lifecycle state logic and transitions based on events, especially from MercadoPago.
    """
    def __init__(self, initial_state: PaymentState):
        self.state = initial_state

    def apply_event(self, event: str) -> PaymentState:
        """
        Transition the payment state machine based on incoming event.
        Args:
            event: The event from payment gateway (e.g., webhook status)
        Returns:
            New PaymentState after applying the event.
        """
        transition_map = {
            (PaymentState.PENDING, "payment_completed"): PaymentState.COMPLETED,
            (PaymentState.PENDING, "payment_failed"): PaymentState.FAILED,
            (PaymentState.COMPLETED, "refund_requested"): PaymentState.REFUNDED,
            (PaymentState.COMPLETED, "refund_completed"): PaymentState.REFUNDED,
            (PaymentState.COMPLETED, "refund_failed"): PaymentState.COMPLETED,  # stays completed
            (PaymentState.FAILED, "retry_payment"): PaymentState.PENDING,
            (PaymentState.REFUNDED, "refund_reversed"): PaymentState.COMPLETED,
        }
        key = (self.state, event)
        if key in transition_map:
            self.state = transition_map[key]
        # else: ignore or log unexpected event
        return self.state

    def can_transition(self, event: str) -> bool:
        """Check if a given event can change state from current state."""
        transition_map = {
            (PaymentState.PENDING, "payment_completed"),
            (PaymentState.PENDING, "payment_failed"),
            (PaymentState.COMPLETED, "refund_requested"),
            (PaymentState.COMPLETED, "refund_completed"),
            (PaymentState.COMPLETED, "refund_failed"),
            (PaymentState.FAILED, "retry_payment"),
            (PaymentState.REFUNDED, "refund_reversed"),
        }
        return (self.state, event) in transition_map

    def get_state(self) -> PaymentState:
        return self.state
