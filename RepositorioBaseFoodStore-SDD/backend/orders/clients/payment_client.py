import httpx
from typing import Optional

class PaymentClient:
    def __init__(self, base_url: str, timeout: float = 3.0):
        self.base_url = base_url
        self.timeout = timeout
        self._circuit_open = False
        self._failures = 0
        self._max_retries = 2

    def _circuit_breaker(self):
        if self._failures >= 2:
            self._circuit_open = True
        return self._circuit_open

    async def authorize_payment(self, order_id: int, amount: float, payment_method: str) -> bool:
        if self._circuit_breaker():
            raise Exception("Payment service unavailable (circuit breaker)")
        for attempt in range(self._max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    resp = await client.post(f"{self.base_url}/payment/authorize", json={"order_id": order_id, "amount": amount, "payment_method": payment_method})
                resp.raise_for_status()
                self._failures = 0
                return resp.json().get("authorized", False)
            except Exception:
                self._failures += 1
        raise Exception("Failed to authorize payment after retries")

    async def refund_payment(self, order_id: int, amount: float) -> bool:
        if self._circuit_breaker():
            raise Exception("Payment service unavailable (circuit breaker)")
        for attempt in range(self._max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    resp = await client.post(f"{self.base_url}/payment/refund", json={"order_id": order_id, "amount": amount})
                resp.raise_for_status()
                self._failures = 0
                return resp.json().get("refunded", False)
            except Exception:
                self._failures += 1
        raise Exception("Failed to refund payment after retries")
