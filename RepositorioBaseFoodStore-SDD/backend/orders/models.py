from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship, JSON
from datetime import datetime
from enum import Enum
from decimal import Decimal

class OrderStatus(str, Enum):
    PENDIENTE = "PENDIENTE"
    CONFIRMADO = "CONFIRMADO"
    EN_PREPARACION = "EN_PREPARACION"
    EN_CAMINO = "EN_CAMINO"
    ENTREGADO = "ENTREGADO"
    CANCELADO = "CANCELADO"

class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", index=True)
    product_id: int = Field(index=True)
    quantity: int
    price: Decimal
    exclusions: List[int] = Field(default=[], sa_type=JSON) 

class Order(SQLModel, table=True):
    __tablename__ = "orders"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    status: OrderStatus = Field(default=OrderStatus.PENDIENTE, index=True)
    total: Decimal
    # Snapshot de dirección
    direccion_calle: str
    direccion_numero: str
    direccion_ciudad: str
    
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    items: List[OrderItem] = Relationship(back_populates="order")

OrderItem.order = Relationship(back_populates="items")
