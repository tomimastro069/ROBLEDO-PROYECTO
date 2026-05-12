from typing import List, Optional
from pydantic import BaseModel, Field as PydanticField
from datetime import datetime
from .models import OrderStatus

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItemCreate]
    total: float

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus]
    items: Optional[List[OrderItemCreate]]
    total: Optional[float]

class OrderItemResponse(OrderItemCreate):
    id: int

class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: OrderStatus
    total: float
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse] = []

    @classmethod
    def from_orm(cls, order):
        return cls(
            id=order.id,
            user_id=order.user_id,
            status=order.status,
            total=order.total,
            created_at=order.created_at,
            updated_at=order.updated_at,
            items=[OrderItemResponse(
                id=i.id, product_id=i.product_id, quantity=i.quantity, price=i.price
            ) for i in getattr(order, 'items', [])]
        )
