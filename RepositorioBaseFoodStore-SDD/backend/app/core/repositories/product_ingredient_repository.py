"""ProductIngredientRepository — Ingredient management for products."""

from typing import List, Optional
from sqlmodel import Session, select
from app.core.shared.base_repository import BaseRepository
from app.core.models import ProductIngredient


class ProductIngredientRepository(BaseRepository[ProductIngredient]):
    """Repository for managing product ingredients."""
    
    def __init__(self, session: Session) -> None:
        super().__init__(session, ProductIngredient)

    def get_by_product_id(self, product_id: int) -> List[ProductIngredient]:
        """Get all ingredients for a product.
        
        Returns:
            List of ingredients
        """
        statement = select(ProductIngredient).where(
            ProductIngredient.product_id == product_id
        )
        return list(self._session.exec(statement).all())

    def get_by_product_id_and_name(self, product_id: int, name: str) -> Optional[ProductIngredient]:
        """Get a specific ingredient by product and name.
        
        Returns:
            Ingredient if found, None otherwise
        """
        statement = select(ProductIngredient).where(
            ProductIngredient.product_id == product_id,
            ProductIngredient.name == name
        )
        return self._session.exec(statement).first()

    def delete_by_product_id(self, product_id: int) -> int:
        """Delete all ingredients for a product.
        
        Returns:
            Number of ingredients deleted
        """
        ingredients = self.get_by_product_id(product_id)
        for ingredient in ingredients:
            self.delete(ingredient)
        return len(ingredients)
