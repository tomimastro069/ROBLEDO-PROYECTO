from pydantic import BaseModel
from datetime import datetime
from typing import List

class OrderCreated(BaseModel):
    order_id: int
    user_id: int
    items: List[dict]
    created_at: datetime

class OrderUpdated(BaseModel):
    order_id: int
    user_id: int
    updated_at: datetime

class OrderCancelled(BaseModel):
    order_id: int
    user_id: int
    cancelled_at: datetime

class OrderSubmitted(BaseModel):
    order_id: int
    user_id: int
    submitted_at: datetime
