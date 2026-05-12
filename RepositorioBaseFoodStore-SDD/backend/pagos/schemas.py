from typing import Optional
from pydantic import BaseModel


class PagoCreate(BaseModel):
    pedido_id: int


class PagoRead(BaseModel):
    pedido_id: int
    preference_id: Optional[str]
    init_point: Optional[str]
    status: str
