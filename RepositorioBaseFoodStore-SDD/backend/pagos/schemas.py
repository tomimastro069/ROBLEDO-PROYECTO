"""Schemas Pydantic para el módulo de pagos."""

from typing import Optional
from pydantic import BaseModel


class PagoCreate(BaseModel):
    pedido_id: int


class PagoRead(BaseModel):
    pedido_id: int
    preference_id: Optional[str] = None
    init_point: Optional[str] = None
    status: str

    class Config:
        from_attributes = True
