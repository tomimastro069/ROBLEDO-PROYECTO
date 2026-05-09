from typing import Optional, List
from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None


class CategoryRead(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class CategoryWithChildren(CategoryRead):
    subcategories: List["CategoryRead"] = []

    class Config:
        from_attributes = True


CategoryWithChildren.model_rebuild()
