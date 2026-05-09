from typing import Optional, List
from pydantic import BaseModel, Field
from app.core.models import OrderStatus
from app.schemas.base import ORMBaseModel

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    historical_price: float = Field(ge=0)

class OrderItemRead(ORMBaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    historical_price: float

class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItemCreate] = Field(min_length=1)

class OrderRead(ORMBaseModel):
    id: int
    status: OrderStatus
    user_id: int
    items: List[OrderItemRead] = []

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
