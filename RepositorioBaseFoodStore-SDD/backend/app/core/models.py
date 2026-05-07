from typing import Optional, List
from datetime import datetime
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
    price: float
    stock: int = Field(default=0)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Optional[Category] = Relationship(back_populates="products")
    ingredients: List[ProductIngredient] = Relationship(back_populates="product")
    allergens: List[ProductAllergen] = Relationship(back_populates="product")
    order_items: List["OrderItem"] = Relationship(back_populates="product")

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    PREPARING = "PREPARING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"

class Order(Base, table=True):
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order")
    payments: List["Payment"] = Relationship(back_populates="order")
    addresses: List["Address"] = Relationship(back_populates="order")

class OrderItem(Base, table=True):
    order_id: Optional[int] = Field(default=None, foreign_key="order.id")
    product_id: Optional[int] = Field(default=None, foreign_key="product.id")
    quantity: int
    historical_price: float
    order: Optional[Order] = Relationship(back_populates="items")
    product: Optional[Product] = Relationship(back_populates="order_items")

class Payment(Base, table=True):
    amount: float
    status: str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    order_id: Optional[int] = Field(default=None, foreign_key="order.id")
    user: Optional[User] = Relationship(back_populates="payments")
    order: Optional[Order] = Relationship(back_populates="payments")

class Address(Base, table=True):
    street: str
    city: str
    state: str
    zip_code: str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    order_id: Optional[int] = Field(default=None, foreign_key="order.id")
    user: Optional[User] = Relationship(back_populates="addresses")
    order: Optional[Order] = Relationship(back_populates="addresses")
