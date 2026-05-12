import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

try:
    import aio_pika
    _AIO_PIKA_AVAILABLE = True
except ImportError:
    _AIO_PIKA_AVAILABLE = False


class EventPublisher:
    def __init__(self, broker_url: str, exchange_name: str = "orders"):
        self.broker_url = broker_url
        self.exchange_name = exchange_name

    async def publish_event(self, event_type: str, event_payload: Any):
        if not _AIO_PIKA_AVAILABLE:
            logger.debug("aio_pika not installed — event %s skipped", event_type)
            return
        connection = await aio_pika.connect_robust(self.broker_url)
        async with connection:
            channel = await connection.channel()
            exchange = await channel.declare_exchange(self.exchange_name, aio_pika.ExchangeType.FANOUT)
            msg = aio_pika.Message(json.dumps({"type": event_type, "payload": event_payload}).encode())
            await exchange.publish(msg, routing_key="")
