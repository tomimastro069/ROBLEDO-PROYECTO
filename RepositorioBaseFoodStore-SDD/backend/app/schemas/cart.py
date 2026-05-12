from pydantic import BaseModel, Field
from decimal import Decimal
from typing import List

class CartItemDTO(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    price: Decimal = Field(gt=0)

class CartValidationRequestDTO(BaseModel):
    items: List[CartItemDTO]
