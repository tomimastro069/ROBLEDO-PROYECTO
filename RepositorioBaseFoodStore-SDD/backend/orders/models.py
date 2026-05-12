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
    product_id: int = Field(foreign_key="product.id", index=True)
    quantity: int
    price_snapshot: Decimal
    exclusions: List[int] = Field(default=[], sa_type=JSON)
    
    # Relaciones
    order: Optional["Order"] = Relationship(back_populates="items")
    product: Optional["Product"] = Relationship(back_populates="order_items")

class Order(SQLModel, table=True):
    __tablename__ = "orders"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    status: OrderStatus = Field(default=OrderStatus.PENDIENTE, index=True)
    total: Decimal
    
    # Snapshot de dirección (para persistencia histórica según US-035)
    direccion_calle: str
    direccion_numero: str
    direccion_ciudad: str
    
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relaciones
    user: Optional["User"] = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    payments: List["Payment"] = Relationship(back_populates="order")
    addresses: List["Address"] = Relationship(back_populates="order")


