"""ProductAllergenRepository — Allergen management for products."""

from typing import List, Optional
from sqlmodel import Session, select
from app.core.shared.base_repository import BaseRepository
from app.core.models import ProductAllergen


class ProductAllergenRepository(BaseRepository[ProductAllergen]):
    """Repository for managing product allergens."""
    
    def __init__(self, session: Session) -> None:
        super().__init__(session, ProductAllergen)

    def get_by_product_id(self, product_id: int) -> List[ProductAllergen]:
        """Get all allergens for a product.
        
        Returns:
            List of allergens
        """
        statement = select(ProductAllergen).where(
            ProductAllergen.product_id == product_id
        )
        return list(self._session.exec(statement).all())

    def get_by_product_id_and_name(self, product_id: int, name: str) -> Optional[ProductAllergen]:
        """Get a specific allergen by product and name.
        
        Returns:
            Allergen if found, None otherwise
        """
        statement = select(ProductAllergen).where(
            ProductAllergen.product_id == product_id,
            ProductAllergen.name == name
        )
        return self._session.exec(statement).first()

    def delete_by_product_id(self, product_id: int) -> int:
        """Delete all allergens for a product.
        
        Returns:
            Number of allergens deleted
        """
        allergens = self.get_by_product_id(product_id)
        for allergen in allergens:
            self.delete(allergen)
        return len(allergens)
