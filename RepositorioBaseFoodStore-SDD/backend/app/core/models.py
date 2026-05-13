from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

class Base(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)

class Role(Base, table=True):
    name: str = Field(unique=True, index=True)
    description: Optional[str] = None
    users: List["User"] = Relationship(back_populates="role")

class User(Base, table=True):
    email: str = Field(unique=True, index=True)
    hashed_password: str
    name: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)
    role_id: Optional[int] = Field(default=None, foreign_key="role.id")
    role: Optional[Role] = Relationship(back_populates="users")
    orders: List["Order"] = Relationship(back_populates="user")
    addresses: List["Address"] = Relationship(back_populates="user")
    payments: List["Payment"] = Relationship(back_populates="user")

class Category(Base, table=True):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = Field(default=None, foreign_key="category.id")
    parent: Optional["Category"] = Relationship(back_populates="subcategories", sa_relationship_kwargs=dict(remote_side="Category.id"))
    subcategories: List["Category"] = Relationship(back_populates="parent")
    products: List["Product"] = Relationship(back_populates="category")
    deleted_at: Optional[datetime] = Field(default=None, description="Soft delete timestamp")

class Ingrediente(Base, table=True):
    nombre: str = Field(unique=True, index=True)
    es_alergeno: bool = Field(default=False)
    deleted_at: Optional[datetime] = Field(default=None)

class ProductIngrediente(Base, table=True):
    product_id: Optional[int] = Field(default=None, foreign_key="product.id", index=True)
    ingrediente_id: Optional[int] = Field(default=None, foreign_key="ingrediente.id", index=True)
    product: Optional["Product"] = Relationship(back_populates="ingredientes")
    ingrediente: Optional["Ingrediente"] = Relationship()

class ProductIngredient(Base, table=True):
    product_id: Optional[int] = Field(default=None, foreign_key="product.id")
    name: str
    product: Optional["Product"] = Relationship(back_populates="ingredients")

class ProductAllergen(Base, table=True):
    product_id: Optional[int] = Field(default=None, foreign_key="product.id")
    name: str
    product: Optional["Product"] = Relationship(back_populates="allergens")

class Product(Base, table=True):
    name: str
    description: Optional[str] = None
    price: Decimal
    stock: int = Field(default=0)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Optional[Category] = Relationship(back_populates="products")
    ingredients: List[ProductIngredient] = Relationship(back_populates="product")
    allergens: List[ProductAllergen] = Relationship(back_populates="product")
    ingredientes: List["ProductIngrediente"] = Relationship(back_populates="product")
    order_items: List["OrderItem"] = Relationship(back_populates="product")
    deleted_at: Optional[datetime] = Field(default=None, description="Soft delete timestamp")

# Eliminadas para evitar conflicto con backend/orders/models.py

class Payment(Base, table=True):
    amount: float
    status: str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    order_id: Optional[int] = Field(default=None, foreign_key="orders.id")
    user: Optional[User] = Relationship(back_populates="payments")
    order: Optional["Order"] = Relationship(back_populates="payments")

class Address(Base, table=True):
    street: str
    numero: Optional[str] = Field(default=None)
    piso: Optional[str] = Field(default=None)
    city: str
    state: str
    zip_code: str
    is_default: bool = Field(default=False)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    order_id: Optional[int] = Field(default=None, foreign_key="orders.id")
    user: Optional[User] = Relationship(back_populates="addresses")
    order: Optional["Order"] = Relationship(back_populates="addresses")
