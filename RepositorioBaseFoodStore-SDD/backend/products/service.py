"""
ProductsService — business logic for product CRUD, ingredient/allergen management, and stock validation.

Responsibilities:
  - CRUD for products
  - Ingredient and allergen management
  - Stock validation and updates
  - Decimal price precision (no float conversions)
  - Soft delete: mark products as deleted (not physically removed)
  - Domain rule validation: category existence, stock availability
  - Transaction coordination via UoW

No HTTP logic here. The router consumes this via DI.
"""

from datetime import datetime
from decimal import Decimal
from typing import List, Tuple, Optional
from fastapi import HTTPException, status

from app.core.uow.unit_of_work import AppUnitOfWork
from app.core.models import Product, ProductIngredient, ProductAllergen


class ProductsService:
    """Product service with CRUD, ingredient management, and stock handling."""
    
    def __init__(self, uow: AppUnitOfWork) -> None:
        self.uow = uow

    # ====================================================================
    # CRUD Operations
    # ====================================================================

    def create(self, name: str, description: Optional[str], price: Decimal, 
               stock: int, category_id: Optional[int]) -> Product:
        """Create a new product.
        
        Args:
            name: Product name
            description: Product description
            price: Product price (Decimal)
            stock: Initial stock quantity
            category_id: Category ID (optional)
            
        Returns:
            Created product
            
        Raises:
            HTTPException(400): Invalid category_id
        """
        with self.uow as uow:
            # Validate: category must exist if specified
            if category_id is not None:
                category = uow.categories.get_by_id(category_id)
                if not category:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Category with id={category_id} not found.",
                    )
            
            product = Product(
                name=name,
                description=description,
                price=price,
                stock=stock,
                category_id=category_id
            )
            uow.products.add(product)
            uow.commit()
            return product

    def get_all(self, limit: int = 50, offset: int = 0) -> Tuple[List[Product], int]:
        """Get all products with pagination.
        
        Returns:
            Tuple of (products, total_count)
        """
        with self.uow as uow:
            # Get count
            all_products = uow.products.get_all()
            total = len(all_products)
            
            # Apply pagination
            products = all_products[offset:offset + limit]
            return products, total

    def get_by_id(self, product_id: int) -> Product:
        """Get product by ID.
        
        Raises:
            HTTPException(404): Product not found
        """
        with self.uow as uow:
            product = uow.products.get_by_id(product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with id={product_id} not found.",
                )
            return product

    def get_by_category(self, category_id: int, limit: int = 50, 
                       offset: int = 0) -> Tuple[List[Product], int]:
        """Get products by category with pagination.
        
        Returns:
            Tuple of (products, total_count)
        """
        with self.uow as uow:
            return uow.products.get_by_category(category_id, limit, offset)

    def search_by_name(self, query: str, limit: int = 50, 
                      offset: int = 0) -> Tuple[List[Product], int]:
        """Search products by name (case-insensitive substring).
        
        Returns:
            Tuple of (products, total_count)
        """
        with self.uow as uow:
            return uow.products.search_by_name(query, limit, offset)

    def update(self, product_id: int, name: Optional[str] = None,
              description: Optional[str] = None, price: Optional[Decimal] = None,
              category_id: Optional[int] = None) -> Product:
        """Update product fields.
        
        Raises:
            HTTPException(404): Product not found
            HTTPException(404): Invalid category_id
        """
        with self.uow as uow:
            product = uow.products.get_by_id(product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with id={product_id} not found.",
                )
            
            # Validate new category if specified
            if category_id is not None and category_id != product.category_id:
                category = uow.categories.get_by_id(category_id)
                if not category:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Category with id={category_id} not found.",
                    )
            
            # Update fields
            if name is not None:
                product.name = name
            if description is not None:
                product.description = description
            if price is not None:
                product.price = price
            if category_id is not None:
                product.category_id = category_id
            
            uow.products.update(product)
            uow.commit()
            return product

    def delete(self, product_id: int) -> None:
        """Soft-delete a product (mark as deleted, don't physically remove).
        
        Raises:
            HTTPException(404): Product not found
        """
        with self.uow as uow:
            product = uow.products.get_by_id(product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with id={product_id} not found.",
                )
            
            # Soft delete: set deleted_at timestamp
            product.deleted_at = datetime.now()
            uow.products.update(product)
            uow.commit()

    # ====================================================================
    # Ingredient Management
    # ====================================================================

    def add_ingredient(self, product_id: int, ingredient_name: str) -> ProductIngredient:
        """Add an ingredient to a product.
        
        Raises:
            HTTPException(404): Product not found
            HTTPException(400): Ingredient already exists
        """
        with self.uow as uow:
            product = uow.products.get_by_id(product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with id={product_id} not found.",
                )
            
            # Check for duplicate
            existing = uow.product_ingredients.get_by_product_id_and_name(
                product_id, ingredient_name
            )
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ingredient '{ingredient_name}' already exists for this product.",
                )
            
            ingredient = ProductIngredient(product_id=product_id, name=ingredient_name)
            uow.product_ingredients.add(ingredient)
            uow.commit()
            return ingredient

    def get_ingredients(self, product_id: int) -> List[ProductIngredient]:
        """Get all ingredients for a product."""
        with self.uow as uow:
            product = uow.products.get_by_id(product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with id={product_id} not found.",
                )
            
            return uow.product_ingredients.get_by_product_id(product_id)

    def remove_ingredient(self, product_id: int, ingredient_id: int) -> None:
        """Remove an ingredient from a product.
        
        Raises:
            HTTPException(404): Product or ingredient not found
        """
        with self.uow as uow:
            product = uow.products.get_by_id(product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with id={product_id} not found.",
                )
            
            ingredient = uow.product_ingredients.get_by_id(ingredient_id)
            if not ingredient or ingredient.product_id != product_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Ingredient with id={ingredient_id} not found for this product.",
                )
            
            uow.product_ingredients.delete(ingredient)
            uow.commit()

    # ====================================================================
    # Allergen Management
    # ====================================================================

    def add_allergen(self, product_id: int, allergen_name: str) -> ProductAllergen:
        """Add an allergen to a product.
        
        Raises:
            HTTPException(404): Product not found
            HTTPException(400): Allergen already exists
        """
        with self.uow as uow:
            product = uow.products.get_by_id(product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with id={product_id} not found.",
                )
            
            # Check for duplicate
            existing = uow.product_allergens.get_by_product_id_and_name(
                product_id, allergen_name
            )
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Allergen '{allergen_name}' already exists for this product.",
                )
            
            allergen = ProductAllergen(product_id=product_id, name=allergen_name)
            uow.product_allergens.add(allergen)
            uow.commit()
            return allergen

    def get_allergens(self, product_id: int) -> List[ProductAllergen]:
        """Get all allergens for a product."""
        with self.uow as uow:
            product = uow.products.get_by_id(product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with id={product_id} not found.",
                )
            
            return uow.product_allergens.get_by_product_id(product_id)

    def remove_allergen(self, product_id: int, allergen_id: int) -> None:
        """Remove an allergen from a product.
        
        Raises:
            HTTPException(404): Product or allergen not found
        """
        with self.uow as uow:
            product = uow.products.get_by_id(product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with id={product_id} not found.",
                )
            
            allergen = uow.product_allergens.get_by_id(allergen_id)
            if not allergen or allergen.product_id != product_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Allergen with id={allergen_id} not found for this product.",
                )
            
            uow.product_allergens.delete(allergen)
            uow.commit()

    # ====================================================================
    # Stock Management & Validation
    # ====================================================================

    def validate_stock_available(self, product_id: int, quantity: int) -> bool:
        """Check if enough stock is available for order.
        
        Returns:
            True if stock >= quantity, False otherwise
        """
        with self.uow as uow:
            return uow.products.validate_stock_available(product_id, quantity)

    def decrease_stock(self, product_id: int, quantity: int) -> Product:
        """Decrease stock by quantity (for order fulfillment).
        
        Raises:
            HTTPException(400): Insufficient stock
            HTTPException(404): Product not found
        """
        with self.uow as uow:
            product = uow.products.decrease_stock(product_id, quantity)
            if product is None:
                # Check if product exists
                existing = uow.products.get_by_id(product_id)
                if not existing:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Product with id={product_id} not found.",
                    )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock. Required: {quantity}, Available: {existing.stock}",
                )
            uow.commit()
            return product

    def increase_stock(self, product_id: int, quantity: int) -> Product:
        """Increase stock by quantity (for restocking or returns).
        
        Raises:
            HTTPException(404): Product not found
        """
        with self.uow as uow:
            product = uow.products.increase_stock(product_id, quantity)
            if product is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with id={product_id} not found.",
                )
            uow.commit()
            return product
