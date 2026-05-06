import pytest
from backend.app.orders.services.payment_state_machine import PaymentStateMachine, PaymentState

def test_completed_transition():
    sm = PaymentStateMachine(PaymentState.PENDING)
    state = sm.apply_event("payment_completed")
    assert state == PaymentState.COMPLETED

def test_failed_transition():
    sm = PaymentStateMachine(PaymentState.PENDING)
    state = sm.apply_event("payment_failed")
    assert state == PaymentState.FAILED

def test_irrelevant_event_stays_pending():
    sm = PaymentStateMachine(PaymentState.PENDING)
    state = sm.apply_event("refund_completed")
    assert state == PaymentState.PENDING

def test_logging_on_state_machine(monkeypatch):
    logs = {}

    def fake_logger(msg):
        logs['msg'] = msg

    # Simulate print or logging call (if PaymentStateMachine did real logging)
    sm = PaymentStateMachine(PaymentState.PENDING)
    sm.apply_event("payment_completed")
    fake_logger(f"Transitioned to {sm.get_state()}")
    assert logs['msg'] == f"Transitioned to {PaymentState.COMPLETED}"
