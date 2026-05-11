"""
Products Router — REST API endpoints for product catalog management.

Endpoints:
  - GET    /products                          → list products (paginated, filterable)
  - GET    /products/{id}                     → get product with ingredients + allergens
  - POST   /products                          → create product (Admin, Gestor Stock)
  - PUT    /products/{id}                     → update product (Admin, Gestor Stock)
  - DELETE /products/{id}                     → soft-delete product (Admin, Gestor Stock)
  - GET    /products/{id}/ingredients         → list ingredients (public)
  - POST   /products/{id}/ingredients         → add ingredient (Admin, Gestor Stock)
  - DELETE /products/{id}/ingredients/{iid}   → remove ingredient (Admin, Gestor Stock)
  - GET    /products/{id}/allergens           → list allergens (public)
  - POST   /products/{id}/allergens           → add allergen (Admin, Gestor Stock)
  - DELETE /products/{id}/allergens/{aid}     → remove allergen (Admin, Gestor Stock)
"""

import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status

from products.schemas import (
    ProductCreate, ProductUpdate, ProductRead,
    ProductWithIngredientsAndAllergens, PaginatedProductResponse,
    ProductIngredientCreate, ProductIngredientRead,
    ProductAllergenCreate, ProductAllergenRead,
)
from products.service import ProductsService
from products.dependencies import get_products_service
from auth.dependencies import get_current_user, require_role
from auth.roles import Role
from auth.schemas import TokenData

logger = logging.getLogger(__name__)
router = APIRouter()

_WRITE_ROLES = (Role.ADMIN, Role.GESTOR_STOCK)


# ============================================================================
# Product CRUD
# ============================================================================

@router.get(
    "",
    response_model=PaginatedProductResponse,
    status_code=status.HTTP_200_OK,
    summary="List products",
)
def list_products(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=200),
    category_id: Optional[int] = Query(default=None),
    search: Optional[str] = Query(default=None),
    service: ProductsService = Depends(get_products_service),
):
    if search:
        items, total = service.search_by_name(search, limit=limit, offset=skip)
    elif category_id is not None:
        items, total = service.get_by_category(category_id, limit=limit, offset=skip)
    else:
        items, total = service.get_all(limit=limit, offset=skip)

    return PaginatedProductResponse(items=items, total=total, limit=limit, offset=skip)


@router.get(
    "/{product_id}",
    response_model=ProductWithIngredientsAndAllergens,
    status_code=status.HTTP_200_OK,
    summary="Get product by ID",
)
def get_product(
    product_id: int,
    service: ProductsService = Depends(get_products_service),
):
    product = service.get_by_id(product_id)
    ingredients = service.get_ingredients(product_id)
    allergens = service.get_allergens(product_id)
    return ProductWithIngredientsAndAllergens(
        **product.model_dump(),
        ingredients=ingredients,
        allergens=allergens,
    )


@router.post(
    "",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create product",
)
def create_product(
    product_in: ProductCreate,
    current_user: TokenData = Depends(require_role(*_WRITE_ROLES)),
    service: ProductsService = Depends(get_products_service),
):
    return service.create(
        name=product_in.name,
        description=product_in.description,
        price=product_in.price,
        stock=product_in.stock,
        category_id=product_in.category_id,
    )


@router.put(
    "/{product_id}",
    response_model=ProductRead,
    status_code=status.HTTP_200_OK,
    summary="Update product",
)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    current_user: TokenData = Depends(require_role(*_WRITE_ROLES)),
    service: ProductsService = Depends(get_products_service),
):
    return service.update(
        product_id=product_id,
        name=product_in.name,
        description=product_in.description,
        price=product_in.price,
        category_id=product_in.category_id,
    )


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Soft-delete product",
)
def delete_product(
    product_id: int,
    current_user: TokenData = Depends(require_role(*_WRITE_ROLES)),
    service: ProductsService = Depends(get_products_service),
):
    service.delete(product_id)


# ============================================================================
# Ingredients sub-resource
# ============================================================================

@router.get(
    "/{product_id}/ingredients",
    response_model=List[ProductIngredientRead],
    status_code=status.HTTP_200_OK,
    summary="List product ingredients",
)
def list_ingredients(
    product_id: int,
    service: ProductsService = Depends(get_products_service),
):
    return service.get_ingredients(product_id)


@router.post(
    "/{product_id}/ingredients",
    response_model=ProductIngredientRead,
    status_code=status.HTTP_201_CREATED,
    summary="Add ingredient to product",
)
def add_ingredient(
    product_id: int,
    ingredient_in: ProductIngredientCreate,
    current_user: TokenData = Depends(require_role(*_WRITE_ROLES)),
    service: ProductsService = Depends(get_products_service),
):
    return service.add_ingredient(product_id, ingredient_in.name)


@router.delete(
    "/{product_id}/ingredients/{ingredient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove ingredient from product",
)
def remove_ingredient(
    product_id: int,
    ingredient_id: int,
    current_user: TokenData = Depends(require_role(*_WRITE_ROLES)),
    service: ProductsService = Depends(get_products_service),
):
    service.remove_ingredient(product_id, ingredient_id)


# ============================================================================
# Allergens sub-resource
# ============================================================================

@router.get(
    "/{product_id}/allergens",
    response_model=List[ProductAllergenRead],
    status_code=status.HTTP_200_OK,
    summary="List product allergens",
)
def list_allergens(
    product_id: int,
    service: ProductsService = Depends(get_products_service),
):
    return service.get_allergens(product_id)


@router.post(
    "/{product_id}/allergens",
    response_model=ProductAllergenRead,
    status_code=status.HTTP_201_CREATED,
    summary="Add allergen to product",
)
def add_allergen(
    product_id: int,
    allergen_in: ProductAllergenCreate,
    current_user: TokenData = Depends(require_role(*_WRITE_ROLES)),
    service: ProductsService = Depends(get_products_service),
):
    return service.add_allergen(product_id, allergen_in.name)


@router.delete(
    "/{product_id}/allergens/{allergen_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove allergen from product",
)
def remove_allergen(
    product_id: int,
    allergen_id: int,
    current_user: TokenData = Depends(require_role(*_WRITE_ROLES)),
    service: ProductsService = Depends(get_products_service),
):
    service.remove_allergen(product_id, allergen_id)
