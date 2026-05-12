import aio_pika
import json
from typing import Any

class EventPublisher:
    def __init__(self, broker_url: str, exchange_name: str = "orders"): 
        self.broker_url = broker_url
        self.exchange_name = exchange_name

    async def publish_event(self, event_type: str, event_payload: Any):
        connection = await aio_pika.connect_robust(self.broker_url)
        async with connection:
            channel = await connection.channel()
            exchange = await channel.declare_exchange(self.exchange_name, aio_pika.ExchangeType.FANOUT)
            msg = aio_pika.Message(json.dumps({"type": event_type, "payload": event_payload}).encode())
            await exchange.publish(msg, routing_key="")
