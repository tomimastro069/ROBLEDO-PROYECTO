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
from app.core.models import Product, ProductIngrediente, Ingrediente


class ProductsService:
    """Product service with CRUD, ingredient management, and stock handling."""
    
    def __init__(self, uow: AppUnitOfWork) -> None:
        self.uow = uow

    # ====================================================================
    # CRUD Operations
    # ====================================================================

    def create(self, name: str, description: Optional[str], price: Decimal, 
               stock: int, category_id: Optional[int], ingredient_ids: Optional[List[int]] = None) -> Product:
        """Create a new product.
        
        Args:
            name: Product name
            description: Product description
            price: Product price (Decimal)
            stock: Initial stock quantity
            category_id: Category ID (optional)
            ingredient_ids: List of ingredient IDs to associate (optional)
            
        Returns:
            Created product
            
        Raises:
            HTTPException(404): Invalid category_id or ingredient_id
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
            uow.session.flush()

            if ingredient_ids:
                for ing_id in ingredient_ids:
                    ing = uow.ingredientes.get_by_id_active(ing_id)
                    if not ing:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Ingredient with id={ing_id} not found.",
                        )
                    uow.ingredientes.add_link(product.id, ing_id)

            uow.commit()
            return product

    def get_all(self, limit: int = 50, offset: int = 0) -> Tuple[List[Product], int]:
        """Get all products with DB-level pagination."""
        with self.uow as uow:
            return uow.products.get_all_paginated(offset=offset, limit=limit)

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
              stock: Optional[int] = None,
              category_id: Optional[int] = None,
              ingredient_ids: Optional[List[int]] = None) -> Product:
        """Update product fields.
        
        Raises:
            HTTPException(404): Product not found
            HTTPException(404): Invalid category_id or ingredient_id
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
            if stock is not None:
                product.stock = stock
            if category_id is not None:
                product.category_id = category_id
            
            uow.products.update(product)

            # Reconcile ingredients if specified
            if ingredient_ids is not None:
                current_ings = uow.ingredientes.get_por_producto(product_id)
                current_ids = {ing.id for ing in current_ings}
                target_ids = set(ingredient_ids)

                # Add new links
                for ing_id in target_ids:
                    if ing_id not in current_ids:
                        ing = uow.ingredientes.get_by_id_active(ing_id)
                        if not ing:
                            raise HTTPException(
                                status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Ingredient with id={ing_id} not found.",
                            )
                        uow.ingredientes.add_link(product_id, ing_id)

                # Remove old links
                for ing_id in current_ids:
                    if ing_id not in target_ids:
                        uow.ingredientes.remove_link(product_id, ing_id)

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

    # Los métodos add_ingredient y remove_ingredient fueron eliminados. 
    # Use IngredientesService para gestionar la asociación de productos con el catálogo global.

    def get_ingredients(self, product_id: int) -> List[Ingrediente]:
        """Get all modular ingredients for a product (includes allergen flag)."""
        with self.uow as uow:
            product = uow.products.get_by_id(product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with id={product_id} not found.",
                )
            
            return uow.ingredientes.get_por_producto(product_id)


    # ====================================================================
    # Allergen Management
    # ====================================================================

    # Los métodos add_allergen y remove_allergen fueron eliminados.

    # El método get_allergens fue eliminado.
    # Los alérgenos ahora se manejan como un flag dentro de cada ingrediente.


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
