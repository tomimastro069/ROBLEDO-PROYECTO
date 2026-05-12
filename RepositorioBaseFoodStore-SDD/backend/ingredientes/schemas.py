from typing import Optional
from pydantic import BaseModel, Field


class IngredienteCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150)
    es_alergeno: bool = False


class IngredienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=150)
    es_alergeno: Optional[bool] = None


class IngredienteRead(BaseModel):
    id: int
    nombre: str
    es_alergeno: bool

    model_config = {"from_attributes": True}
