"""
Categories Router — REST API endpoints for hierarchical category management.

Endpoints:
  - GET    /categories              → list all categories
  - GET    /categories/{id}         → get single category with hierarchy
  - POST   /categories              → create category (Admin only)
  - PUT    /categories/{id}         → update category (Admin, Stock Manager)
  - DELETE /categories/{id}         → soft delete category (Admin only)

The router depends on CategoriesService and uses FastAPI's dependency injection
to enforce RBAC and manage transactions.
"""

import logging
from typing import List
from fastapi import APIRouter, Depends, status

from categories.schemas import CategoryCreate, CategoryUpdate, CategoryRead, CategoryWithChildren
from categories.service import CategoriesService
from categories.dependencies import get_categories_service
from auth.dependencies import get_current_user, require_role
from auth.roles import Role
from auth.schemas import TokenData

logger = logging.getLogger(__name__)
router = APIRouter()


# ============================================================================
# GET endpoints (public, no auth required)
# ============================================================================


@router.get(
    "",
    response_model=List[CategoryRead],
    status_code=status.HTTP_200_OK,
    summary="List all categories",
    description="Get all top-level and nested categories. Public endpoint."
)
def list_categories(
    skip: int = 0,
    limit: int = 100,
    categories_service: CategoriesService = Depends(get_categories_service),
):
    """
    List all categories with optional pagination.
    
    - **skip**: number of records to skip (default 0)
    - **limit**: number of records to return (default 100, max 1000)
    """
    logger.info(f"GET /categories (skip={skip}, limit={limit})")
    # TODO: Implement pagination logic
    return categories_service.get_all()


@router.get(
    "/{category_id}",
    response_model=CategoryWithChildren,
    status_code=status.HTTP_200_OK,
    summary="Get category by ID",
    description="Get a single category with all its nested subcategories (hierarchy)."
)
def get_category(
    category_id: int,
    categories_service: CategoriesService = Depends(get_categories_service),
):
    """
    Get a single category by ID, including all subcategories.
    
    Returns 404 if category doesn't exist.
    """
    logger.info(f"GET /categories/{category_id}")
    return categories_service.get_by_id(category_id)


# ============================================================================
# POST endpoint (create, Admin only)
# ============================================================================


@router.post(
    "",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create new category",
    description="Create a new category. Requires Admin role."
)
def create_category(
    category_in: CategoryCreate,
    current_user: TokenData = Depends(require_role(Role.ADMIN)),
    categories_service: CategoriesService = Depends(get_categories_service),
):
    """
    Create a new category.
    
    - **name**: category name (required, 1-100 chars)
    - **description**: optional description
    - **parent_id**: optional parent category ID (for hierarchy)
    
    Returns 201 Created with the created category.
    Returns 403 Forbidden if user is not Admin.
    Returns 400 Bad Request if parent_id is invalid.
    """
    logger.info(f"POST /categories — user_id={current_user.sub}, name={category_in.name}")
    return categories_service.create(category_in)


# ============================================================================
# PUT endpoint (update, Admin or Stock Manager)
# ============================================================================


@router.put(
    "/{category_id}",
    response_model=CategoryRead,
    status_code=status.HTTP_200_OK,
    summary="Update category",
    description="Update a category by ID. Requires Admin or Stock Manager role."
)
def update_category(
    category_id: int,
    category_in: CategoryUpdate,
    current_user: TokenData = Depends(require_role(Role.ADMIN, Role.GESTOR_STOCK)),
    categories_service: CategoriesService = Depends(get_categories_service),
):
    """
    Update an existing category.
    
    - **category_id**: ID of category to update
    - **name**, **description**, **parent_id**: fields to update (all optional)
    
    Returns 200 OK with the updated category.
    Returns 403 Forbidden if user lacks required role.
    Returns 404 Not Found if category doesn't exist.
    Returns 400 Bad Request if parent_id is invalid.
    """
    logger.info(f"PUT /categories/{category_id} — user_id={current_user.sub}")
    return categories_service.update(category_id, category_in)


# ============================================================================
# DELETE endpoint (soft delete, Admin only)
# ============================================================================


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete category",
    description="Soft-delete a category by ID (mark as deleted). Requires Admin role."
)
def delete_category(
    category_id: int,
    current_user: TokenData = Depends(require_role(Role.ADMIN)),
    categories_service: CategoriesService = Depends(get_categories_service),
):
    """
    Delete (soft delete) a category.
    
    - **category_id**: ID of category to delete
    
    Returns 204 No Content on success.
    Returns 403 Forbidden if user is not Admin.
    Returns 404 Not Found if category doesn't exist.
    """
    logger.info(f"DELETE /categories/{category_id} — user_id={current_user.sub}")
    categories_service.delete(category_id)
