from typing import Optional, List
from pydantic import BaseModel, Field

from app.schemas.base import ORMBaseModel

class CategoryCreate(BaseModel):
    name: str = Field(min_length=1)
    description: Optional[str] = None
    parent_id: Optional[int] = None

class CategoryRead(ORMBaseModel):
    id: int
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = None
    parent_id: Optional[int] = None
