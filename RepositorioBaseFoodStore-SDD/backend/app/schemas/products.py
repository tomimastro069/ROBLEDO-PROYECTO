from typing import Optional, List
from pydantic import BaseModel, Field

from app.schemas.base import ORMBaseModel

class ProductCreate(BaseModel):
    name: str = Field(min_length=1)
    description: Optional[str] = None
    price: float = Field(gt=0, description="Price must be strictly greater than 0")
    stock: int = Field(default=0, ge=0, description="Stock cannot be negative")
    category_id: Optional[int] = None

class ProductRead(ORMBaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category_id: Optional[int] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    stock: Optional[int] = Field(default=None, ge=0)
    category_id: Optional[int] = None
