"""Pydantic schemas for Product, ProductIngredient, ProductAllergen with Decimal support."""

from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


# ====================================================================
# Product Schemas
# ====================================================================

class ProductBase(BaseModel):
    """Base schema for product data."""
    name: str = Field(..., min_length=1, max_length=200, description="Product name")
    description: Optional[str] = Field(None, max_length=1000, description="Product description")
    price: Decimal = Field(..., gt=0, decimal_places=2, description="Product price (Decimal with 2 decimal places)")
    stock: int = Field(default=0, ge=0, description="Available stock quantity")
    category_id: Optional[int] = Field(None, description="Category ID")


class ProductCreate(ProductBase):
    """Schema for creating a new product."""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating a product (all fields optional)."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[Decimal] = Field(None, decimal_places=2)
    category_id: Optional[int] = None


class ProductRead(ProductBase):
    """Schema for reading/returning product data."""
    id: int
    
    model_config = ConfigDict(from_attributes=True)


# ====================================================================
# ProductIngredient Schemas
# ====================================================================

class ProductIngredientBase(BaseModel):
    """Base schema for product ingredient."""
    name: str = Field(..., min_length=1, max_length=200, description="Ingredient name")


class ProductIngredientCreate(ProductIngredientBase):
    """Schema for adding an ingredient to a product."""
    pass


class ProductIngredientRead(ProductIngredientBase):
    """Schema for reading ingredient data."""
    id: int
    product_id: int
    
    model_config = ConfigDict(from_attributes=True)


# ====================================================================
# ProductAllergen Schemas
# ====================================================================

class ProductAllergenBase(BaseModel):
    """Base schema for product allergen."""
    name: str = Field(..., min_length=1, max_length=200, description="Allergen name (e.g., 'peanuts', 'gluten')")


class ProductAllergenCreate(ProductAllergenBase):
    """Schema for adding an allergen to a product."""
    pass


class ProductAllergenRead(ProductAllergenBase):
    """Schema for reading allergen data."""
    id: int
    product_id: int
    
    model_config = ConfigDict(from_attributes=True)


# ====================================================================
# Composite Schemas (for responses with nested data)
# ====================================================================

from ingredientes.schemas import IngredienteRead

class ProductWithIngredients(ProductRead):
    """Schema for product with nested modular ingredients."""
    ingredientes: List[IngredienteRead] = []
    
    model_config = ConfigDict(from_attributes=True)


# ====================================================================
# Response Schemas (for paginated results)
# ====================================================================

class PaginatedProductResponse(BaseModel):
    """Paginated response for product list."""
    items: List[ProductRead]
    total: int
    limit: int
    offset: int
