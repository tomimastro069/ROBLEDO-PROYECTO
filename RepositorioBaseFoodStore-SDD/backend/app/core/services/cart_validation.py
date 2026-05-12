from typing import List
from app.schemas.cart import CartItemDTO

class CartValidationError(Exception):
    pass

class CartValidationService:
    def __init__(self, products_service):
        self.products_service = products_service

    def validate_cart(self, items: List[CartItemDTO]) -> None:
        for item in items:
            product = self.products_service.get_by_id(item.product_id)
            if product is None:
                raise CartValidationError(f"Product {item.product_id} not found")
            if product.price != item.price:
                raise CartValidationError(
                    f"Price mismatch for product {item.product_id}: sent={item.price}, db={product.price}"
                )
            if product.stock < item.quantity:
                raise CartValidationError(
                    f"Not enough stock for product {item.product_id}: requested={item.quantity}, available={product.stock}"
                )
