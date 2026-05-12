import httpx
from typing import Optional

class CatalogClient:
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

    async def get_product_price(self, product_id: int) -> Optional[float]:
        if self._circuit_breaker():
            raise Exception("Catalog service unavailable (circuit breaker)")
        for attempt in range(self._max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    resp = await client.get(f"{self.base_url}/catalog/product/{product_id}/price")
                resp.raise_for_status()
                self._failures = 0
                return resp.json().get("price")
            except Exception:
                self._failures += 1
        raise Exception("Failed to fetch product price after retries")
