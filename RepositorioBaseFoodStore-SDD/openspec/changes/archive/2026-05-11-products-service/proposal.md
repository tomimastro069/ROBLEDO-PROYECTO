## Why

The product catalog is the core of the e-commerce platform. Without a robust ProductsService layer, the frontend has no way to fetch, filter, or manage the catalog, and downstream services (cart, orders) cannot validate product data or snapshots. This change establishes the business logic for product management before exposing it via HTTP endpoints in the next change (products-api).

## What Changes

- Create `ProductsRepository` extending `BaseRepository[Product]` with specialized queries: `get_by_category()`, `search_by_name()`, `get_all_paginated()`.
- Create `ProductsService` orchestrating CRUD operations, ingredient/allergen management, stock validation, and soft deletes via the Unit of Work.
- Update the `Product` model to use `Decimal` for price (precision) instead of `float`.
- Add `ProductIngredientRepository` and `ProductAllergenRepository` for managing related entities.
- Register all repositories in `AppUnitOfWork` so ProductsService can access them atomically.
- Define Pydantic schemas (`ProductCreate`, `ProductUpdate`, `ProductRead`, `IngredientCreate`, `AllergenRead`) for request/response validation.

## Capabilities

### New Capabilities

- `product-catalog`: CRUD logic for products, ingredient/allergen management, stock validation, and soft deletes.
- `product-repository`: Data access layer with queries for filtering, pagination, and category-based browsing.

### Modified Capabilities

- `domain-models`: Update Product model to use Decimal for price precision.

## Impact

- **Backend modules affected**: `backend/products/` (new), `backend/app/core/models.py` (Product price type), `backend/app/core/repositories/` (ProductsRepository), `backend/app/core/uow/unit_of_work.py` (register ProductsRepository).
- **No HTTP endpoints yet** — those come in products-api (change #16).
- **Downstream dependencies**: cart-service, orders-service, and products-api all depend on this service being stable and correct.
- **Database**: No new migrations required (Product, ProductIngredient, ProductAllergen tables already exist from domain-models change).
