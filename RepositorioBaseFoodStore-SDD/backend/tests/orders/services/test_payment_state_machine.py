import unittest
from backend.app.orders.services.payment_state_machine import PaymentStateMachine, PaymentState

class TestPaymentStateMachine(unittest.TestCase):
    def test_initial_state(self):
        sm = PaymentStateMachine(PaymentState.PENDING)
        self.assertEqual(sm.get_state(), PaymentState.PENDING)

    def test_payment_completed_transition(self):
        sm = PaymentStateMachine(PaymentState.PENDING)
        sm.apply_event("payment_completed")
        self.assertEqual(sm.get_state(), PaymentState.COMPLETED)

    def test_payment_failed_transition(self):
        sm = PaymentStateMachine(PaymentState.PENDING)
        sm.apply_event("payment_failed")
        self.assertEqual(sm.get_state(), PaymentState.FAILED)

    def test_refunded_transition_from_completed(self):
        sm = PaymentStateMachine(PaymentState.COMPLETED)
        sm.apply_event("refund_requested")
        self.assertEqual(sm.get_state(), PaymentState.REFUNDED)

        sm = PaymentStateMachine(PaymentState.COMPLETED)
        sm.apply_event("refund_completed")
        self.assertEqual(sm.get_state(), PaymentState.REFUNDED)

    def test_refund_failed_from_completed(self):
        sm = PaymentStateMachine(PaymentState.COMPLETED)
        sm.apply_event("refund_failed")
        self.assertEqual(sm.get_state(), PaymentState.COMPLETED)

    def test_retry_payment_from_failed(self):
        sm = PaymentStateMachine(PaymentState.FAILED)
        sm.apply_event("retry_payment")
        self.assertEqual(sm.get_state(), PaymentState.PENDING)

    def test_refund_reversed_from_refunded(self):
        sm = PaymentStateMachine(PaymentState.REFUNDED)
        sm.apply_event("refund_reversed")
        self.assertEqual(sm.get_state(), PaymentState.COMPLETED)

    def test_invalid_transition(self):
        sm = PaymentStateMachine(PaymentState.PENDING)
        sm.apply_event("refund_requested")  # not valid
        self.assertEqual(sm.get_state(), PaymentState.PENDING)

    def test_can_transition(self):
        sm = PaymentStateMachine(PaymentState.PENDING)
        self.assertTrue(sm.can_transition("payment_completed"))
        self.assertTrue(sm.can_transition("payment_failed"))
        self.assertFalse(sm.can_transition("refund_requested"))

if __name__ == "__main__":
    unittest.main()
