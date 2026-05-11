"""ProductsRepository — Product CRUD and specialized queries with soft-delete support."""

from typing import Optional, List, Tuple
from decimal import Decimal
from sqlmodel import Session, select, func
from app.core.shared.base_repository import BaseRepository
from app.core.models import Product


class ProductsRepository(BaseRepository[Product]):
    """Product repository with specialized queries and soft-delete filtering."""
    
    def __init__(self, session: Session) -> None:
        super().__init__(session, Product)

    # Override get_by_id to apply soft-delete filter
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID, excluding soft-deleted products."""
        statement = select(Product).where(
            (Product.id == product_id) &
            (Product.deleted_at.is_(None))
        )
        return self._session.exec(statement).first()

    # Override get_all to apply soft-delete filter
    def get_all(self) -> List[Product]:
        """Get all non-deleted products."""
        statement = select(Product).where(Product.deleted_at.is_(None))
        return list(self._session.exec(statement).all())

    # Specialized queries (KISS approach)

    def get_by_category(self, category_id: int, limit: int = 50, offset: int = 0) -> Tuple[List[Product], int]:
        """Get products by category with pagination, excluding soft-deleted.
        
        Returns:
            Tuple of (products, total_count)
        """
        # Get count (excluding soft-deleted)
        count_stmt = select(func.count(Product.id)).where(
            (Product.category_id == category_id) &
            (Product.deleted_at.is_(None))
        )
        total = self._session.exec(count_stmt).one()
        
        # Get paginated results (excluding soft-deleted)
        stmt = select(Product).where(
            (Product.category_id == category_id) &
            (Product.deleted_at.is_(None))
        ).offset(offset).limit(limit)
        
        products = list(self._session.exec(stmt).all())
        return products, total

    def search_by_name(self, query: str, limit: int = 50, offset: int = 0) -> Tuple[List[Product], int]:
        """Search products by name (case-insensitive substring match), excluding soft-deleted.
        
        Returns:
            Tuple of (products, total_count)
        """
        # Get count (excluding soft-deleted)
        count_stmt = select(func.count(Product.id)).where(
            (Product.name.ilike(f"%{query}%")) &
            (Product.deleted_at.is_(None))
        )
        total = self._session.exec(count_stmt).one()
        
        # Get paginated results (excluding soft-deleted)
        stmt = select(Product).where(
            (Product.name.ilike(f"%{query}%")) &
            (Product.deleted_at.is_(None))
        ).offset(offset).limit(limit)
        
        products = list(self._session.exec(stmt).all())
        return products, total

    def validate_stock_available(self, product_id: int, quantity: int) -> bool:
        """Check if enough stock is available for the product.
        
        Returns:
            True if stock >= quantity, False otherwise
        """
        product = self.get_by_id(product_id)
        if product is None:
            return False
        return product.stock >= quantity

    def decrease_stock(self, product_id: int, quantity: int) -> Optional[Product]:
        """Decrease product stock by quantity.
        
        Returns:
            Updated product if successful, None if insufficient stock
        """
        product = self.get_by_id(product_id)
        if product is None or product.stock < quantity:
            return None
        
        product.stock -= quantity
        return self.update(product)

    def increase_stock(self, product_id: int, quantity: int) -> Optional[Product]:
        """Increase product stock by quantity.
        
        Returns:
            Updated product
        """
        product = self.get_by_id(product_id)
        if product is None:
            return None
        
        product.stock += quantity
        return self.update(product)
