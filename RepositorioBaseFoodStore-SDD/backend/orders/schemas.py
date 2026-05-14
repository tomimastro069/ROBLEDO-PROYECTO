from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from decimal import Decimal
from .models import OrderStatus

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    exclusions: List[int] = []

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemRead(OrderItemBase):
    id: int
    price_snapshot: Decimal
    
    model_config = ConfigDict(from_attributes=True)

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    shipping_address_id: int

class OrderRead(BaseModel):
    id: int
    user_id: int
    status: OrderStatus
    total: Decimal
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemRead]
    
    # Snapshots de dirección
    direccion_calle: str
    direccion_numero: str
    direccion_ciudad: str
    
    # Pago
    forma_pago_codigo: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class OrderAdminRead(OrderRead):
    user_email: Optional[str] = None
    # Aquí podríamos agregar el historial de estados si fuera necesario

class StateChangeRequest(BaseModel):
    new_status: Optional[OrderStatus] = None
    reason: Optional[str] = "Sin motivo especificado"
