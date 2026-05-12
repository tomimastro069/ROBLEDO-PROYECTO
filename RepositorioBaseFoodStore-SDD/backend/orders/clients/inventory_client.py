import httpx
from typing import Optional

class InventoryClient:
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

    async def verify_and_deduct_stock(self, product_id: int, quantity: int) -> bool:
        if self._circuit_breaker():
            raise Exception("Inventory service unavailable (circuit breaker)")
        for attempt in range(self._max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    resp = await client.post(f"{self.base_url}/inventory/verify-deduct", json={"product_id": product_id, "quantity": quantity})
                resp.raise_for_status()
                self._failures = 0
                return resp.json().get("success", False)
            except Exception:
                self._failures += 1
        raise Exception("Failed to verify and deduct stock after retries")
