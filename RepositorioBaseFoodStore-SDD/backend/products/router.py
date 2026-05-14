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
    ProductWithIngredients, PaginatedProductResponse,
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
    response_model=ProductWithIngredients,
    status_code=status.HTTP_200_OK,
    summary="Get product by ID",
)
def get_product(
    product_id: int,
    service: ProductsService = Depends(get_products_service),
):
    product = service.get_by_id(product_id)
    ingredientes = service.get_ingredients(product_id)
    return ProductWithIngredients(
        **product.model_dump(),
        ingredientes=ingredientes,
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
        stock=product_in.stock,
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


# --- Sub-recursos de ingredientes y alérgenos eliminados. 
# La gestión se realiza a través de /api/v1/ingredientes ---
