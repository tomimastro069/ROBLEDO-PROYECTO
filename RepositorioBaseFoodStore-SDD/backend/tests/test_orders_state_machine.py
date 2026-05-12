import pytest
from orders.state_machine import OrderStateMachine
from orders.models import OrderStatus
from orders.exceptions import InvalidStatusTransition

def test_valid_transitions():
    # DRAFT -> SUBMITTED
    OrderStateMachine.validate_transition(OrderStatus.DRAFT, OrderStatus.SUBMITTED)
    # SUBMITTED -> PROCESSING
    OrderStateMachine.validate_transition(OrderStatus.SUBMITTED, OrderStatus.PROCESSING)
    # SUBMITTED -> CANCELLED
    OrderStateMachine.validate_transition(OrderStatus.SUBMITTED, OrderStatus.CANCELLED)
    # PROCESSING -> COMPLETED
    OrderStateMachine.validate_transition(OrderStatus.PROCESSING, OrderStatus.COMPLETED)
    # PROCESSING -> CANCELLED
    OrderStateMachine.validate_transition(OrderStatus.PROCESSING, OrderStatus.CANCELLED)

def test_invalid_transitions():
    # DRAFT cannot skip to COMPLETED
    with pytest.raises(InvalidStatusTransition):
        OrderStateMachine.validate_transition(OrderStatus.DRAFT, OrderStatus.COMPLETED)
    
    # CANCELLED is a final state
    with pytest.raises(InvalidStatusTransition):
        OrderStateMachine.validate_transition(OrderStatus.CANCELLED, OrderStatus.SUBMITTED)
    
    # COMPLETED is a final state
    with pytest.raises(InvalidStatusTransition):
        OrderStateMachine.validate_transition(OrderStatus.COMPLETED, OrderStatus.CANCELLED)

def test_transition_to_self_is_invalid_by_default():
    # Unless explicitly allowed, transitions to same state are not in the allowed map
    with pytest.raises(InvalidStatusTransition):
        OrderStateMachine.validate_transition(OrderStatus.SUBMITTED, OrderStatus.SUBMITTED)
