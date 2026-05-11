## 1. Model Updates

- [x] 1.1 Update Product model: change `price: float` to `price: Decimal` in `backend/app/core/models.py`
- [x] 1.2 Create Alembic migration to alter `products.price` column type from `REAL` to `NUMERIC(10,2)` in PostgreSQL
- [x] 1.3 Run migration to apply schema changes to the database

## 2. Repository Layer

- [x] 2.1 Create `ProductsRepository` in `backend/app/core/repositories/products_repository.py` extending `BaseRepository[Product]`
- [x] 2.2 Implement `get_by_category(category_id: int, skip: int, limit: int) → tuple[list[Product], int]` query with pagination
- [x] 2.3 Implement `search_by_name(query: str, skip: int, limit: int) → tuple[list[Product], int]` query with ILIKE and pagination
- [x] 2.4 Implement `validate_stock_available(product_id: int, quantity: int) → bool` query
- [x] 2.5 Implement `get_by_name(name: str) → Optional[Product]` for uniqueness checks
- [x] 2.6 Create `ProductIngredientRepository` in `backend/app/core/repositories/product_ingredient_repository.py`
- [x] 2.7 Implement `get_by_product(product_id: int) → list[ProductIngredient]` in ProductIngredientRepository
- [x] 2.8 Create `ProductAllergenRepository` in `backend/app/core/repositories/product_allergen_repository.py`
- [x] 2.9 Verify all repository queries filter `deleted_at IS NULL` for soft delete respect
- [x] 2.10 Update `backend/app/core/repositories/__init__.py` to export new repositories

## 3. Unit of Work Integration

- [x] 3.1 Register `ProductsRepository` in `AppUnitOfWork` (add to `__enter__` method)
- [x] 3.2 Register `ProductIngredientRepository` in `AppUnitOfWork`
- [x] 3.3 Register `ProductAllergenRepository` in `AppUnitOfWork`
- [x] 3.4 Verify UoW type hints updated in `backend/app/core/uow/unit_of_work.py`

## 4. Service Layer

- [x] 4.1 Create `ProductsService` in `backend/products/service.py` with `__init__(self, uow: AppUnitOfWork)`
- [x] 4.2 Implement `create(data: ProductCreate) → Product` with validation (name unique check, price > 0)
- [x] 4.3 Implement `read(product_id: int) → Optional[Product]` returning None if not found or soft-deleted
- [x] 4.4 Implement `read_all(skip: int = 0, limit: int = 100) → tuple[list[Product], int]` with pagination
- [x] 4.5 Implement `update(product_id: int, data: ProductUpdate) → Product` with updated_at timestamp
- [x] 4.6 Implement `delete(product_id: int) → Product` (soft delete: set deleted_at timestamp)
- [x] 4.7 Implement `add_ingredient(product_id: int, ingredient: IngredientCreate) → ProductIngredient`
- [x] 4.8 Implement `get_ingredients(product_id: int) → list[ProductIngredient]`
- [x] 4.9 Implement `remove_ingredient(product_id: int, ingredient_id: int) → None`
- [x] 4.10 Implement `mark_allergen(ingredient_id: int, is_allergen: bool) → ProductIngredient`
- [x] 4.11 Implement `search_by_category(category_id: int, skip: int = 0, limit: int = 100) → tuple[list[Product], int]`
- [x] 4.12 Implement `validate_stock_available(product_id: int, quantity: int) → bool`
- [x] 4.13 Verify all service methods use `with self.uow as uow:` context manager for atomicity

## 5. Pydantic Schemas

- [x] 5.1 Create `ProductCreate` schema in `backend/products/schemas.py` (name, description, price, category_id, stock)
- [x] 5.2 Create `ProductUpdate` schema (name, description, price, category_id, stock - all optional)
- [x] 5.3 Create `ProductRead` schema (id, name, description, price, category_id, stock, ingredients, created_at, updated_at)
- [x] 5.4 Create `IngredientCreate` schema (name, is_allergen)
- [x] 5.5 Create `IngredientRead` schema (id, product_id, name, is_allergen)
- [x] 5.6 Add Decimal JSON encoder configuration for price serialization (Decimal → str in API responses)
- [x] 5.7 Add validators: price > 0, stock >= 0, name not empty

## 6. Dependencies Injection

- [x] 6.1 Create `get_products_service()` dependency in `backend/products/dependencies.py` returning ProductsService
- [x] 6.2 Verify dependency uses `Depends(get_uow)` to inject AppUnitOfWork

## 7. Integration & Verification

- [x] 7.1 Create `backend/products/__init__.py` with module initialization
- [x] 7.2 Verify imports work: `from backend.products.service import ProductsService`
- [x] 7.3 Test ProductsService instantiation with mock UoW (manual test for now)
- [x] 7.4 Verify soft delete behavior: call delete(), then read() should return None
- [x] 7.5 Verify pagination: add 50 test products, paginate with limit=20, verify total_count
- [x] 7.6 Verify category filtering: products from different categories, filter by one, verify only that category returns
- [x] 7.7 Verify ingredient management: add/remove ingredients, verify list is correct
- [x] 7.8 Create smoke test script in `backend/tests/` to verify service layer works end-to-end with real DB

## 8. Documentation

- [x] 8.1 Add docstrings to all ProductsService methods
- [x] 8.2 Add docstrings to all ProductsRepository methods
- [x] 8.3 Document error cases and exceptions raised by each method
- [x] 8.4 Create CHANGELOG entry for this change
