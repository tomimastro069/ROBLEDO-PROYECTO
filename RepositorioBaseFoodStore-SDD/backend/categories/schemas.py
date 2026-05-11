from typing import Optional, List
from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    """Base schema for category data."""
    name: str = Field(..., min_length=1, max_length=100, description="Category name")
    description: Optional[str] = Field(None, max_length=500, description="Category description")
    parent_id: Optional[int] = Field(None, description="Parent category ID for hierarchy")


class CategoryCreate(CategoryBase):
    """Schema for creating a new category."""
    pass


class CategoryUpdate(BaseModel):
    """Schema for updating a category."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    parent_id: Optional[int] = None


class CategoryRead(CategoryBase):
    """Schema for reading/returning category data."""
    id: int

    class Config:
        from_attributes = True


class CategoryWithChildren(CategoryRead):
    """Schema for category with nested children (hierarchy)."""
    subcategories: List["CategoryRead"] = []

    class Config:
        from_attributes = True


CategoryWithChildren.model_rebuild()
