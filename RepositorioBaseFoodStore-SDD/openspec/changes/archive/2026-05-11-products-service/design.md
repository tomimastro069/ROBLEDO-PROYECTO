## Context

The e-commerce platform follows a layered backend architecture: `Router → Service → UoW → Repository → Model`. The `products-service` sits at the **Service layer**, receiving requests from routers and delegating data access to repositories through a Unit of Work. Products are central to the catalog, cart, and order flows.

**Current State:**
- Product, ProductIngredient, ProductAllergen models exist in `backend/app/core/models.py`.
- `CategoriesService` provides a working reference implementation of the Service layer.
- `BaseRepository[T]` and `CategoryRepository` establish the pattern for repositories.
- `AppUnitOfWork` orchestrates all repositories atomically.

**Constraints:**
- All repository operations must respect soft deletes (filter `deleted_at IS NULL`).
- Product price must be `Decimal` for financial precision.
- Ingredients are product-specific (not shared globally).
- Stock is an integer ≥ 0; never goes negative within service logic (validated at order-time).

## Goals / Non-Goals

**Goals:**
- Establish `ProductsService` as the single source of truth for product business logic.
- Implement `ProductsRepository` with queries for CRUD, category filtering, pagination, and stock validation.
- Support ingredient and allergen management (add, remove, mark as allergen).
- Provide soft-delete semantics (mark `deleted_at`, never hard-delete).
- Ensure atomicity: all operations use UoW context manager for transaction safety.
- Define clear contracts via Pydantic schemas for request/response validation.

**Non-Goals:**
- Full-text search (TSVECTOR / PostgreSQL FTS) — deferred to future change if needed.
- Admin-level soft-delete recovery queries — will add in admin module change.
- Product image/media management — out of scope for this change.
- Price history / audit trail — out of scope (only snapshots at order time).

## Decisions

### Decision: Price as Decimal

**Choice**: Use `Decimal` (from Python's `decimal` module and SQLModel) instead of `float`.

**Alternatives considered**:
- `float`: Simple but loses precision in financial calculations (0.1 + 0.2 ≠ 0.3).
- `str`: Avoids rounding issues but harder to validate and compare.
- `int` (cents): Requires conversion but avoids floating-point entirely.

**Rationale**: Decimal preserves financial precision, can be validated, and converts cleanly to/from API responses. This is industry standard for prices.

**Impact on Model**: `backend/app/core/models.py` Product.price changes from `float` to `Decimal`.

### Decision: Repository Query Methods

**Choice**: Implement specialized queries in `ProductsRepository`:
- `get_by_category(category_id: int, skip: int, limit: int) → (items, total)`
- `search_by_name(query: str, skip: int, limit: int) → (items, total)`
- `validate_stock_available(product_id: int, qty: int) → bool`

**Alternatives considered**:
- GraphQL-style query builder (too heavy for current scope).
- Full-text search with PostgreSQL TSVECTOR (deferred — use simple LIKE for now).
- Single generic `filter()` method (too vague, unclear what queries are possible).

**Rationale**: KISS. These 3 queries unlock products-api and cart-service without over-engineering. Pagination returns both items and total_count for frontend controls.

### Decision: Ingredients Management

**Choice**: Ingredients are **product-specific** (stored as ProductIngredient rows with product_id). No global Ingredient table.

**Alternatives considered**:
- Global Ingredient catalog (shared across products) — requires Product-Ingredient M2M junction table, more complex.
- Enum of predefined ingredients — inflexible.

**Rationale**: Simpler schema for now. Each product defines its own ingredients. If global ingredient sharing becomes a requirement later, it's a backward-compatible migration.

### Decision: Soft Delete Filtering

**Choice**: Every query in `ProductsRepository` **explicitly filters `deleted_at IS NULL`**. No automatic global filter.

**Alternatives considered**:
- Hybrid table (active products in `products`, deleted in `products_archive`) — complexity without benefit.
- ORM-level hybrid property (SQLAlchemy offers this) — still requires per-query override for admin views.

**Rationale**: Explicit filters are clearer (developers see the intent), and allow easy admin overrides (just remove the filter). Matches CategoriesRepository pattern already in codebase.

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| **Decimal type not handled by Pydantic/API response** | Import `pydantic.json_encoders`, configure serialization to convert Decimal → str for JSON. Test this early. |
| **Pagination queries are N+1 if not careful** | Use SQLAlchemy's `select().where()` syntax, not lazy loading. Test with small datasets to ensure no extra queries. |
| **Soft deletes lead to orphaned ingredients** | Implement cascade soft-delete: when product is soft-deleted, mark ingredients as deleted too (or just leave them). For now, leave orphaned; add cleanup in admin module later. |
| **Search by LIKE on name is slow with millions of products** | Add PostgreSQL B-tree index on `Product.name`. Upgrade to full-text search later if needed. |
| **Stock validation at service level, not at order time** | This is intentional — `validate_stock_available()` is a precondition check. Final stock decrement happens in orders-service within transaction. |

## Migration Plan

1. Update `Product` model in `backend/app/core/models.py`: change `price: float` to `price: Decimal`.
2. Create new migration file with Alembic to alter `products.price` column type (PostgreSQL: `NUMERIC` with precision).
3. Create `ProductsRepository`, `ProductIngredientRepository`, `ProductAllergenRepository` in `backend/app/core/repositories/`.
4. Create `ProductsService` in `backend/products/service.py`.
5. Create schemas in `backend/products/schemas.py` (ProductCreate, ProductUpdate, ProductRead, etc.).
6. Register repositories in `AppUnitOfWork`.
7. Run tests (when test infrastructure available).

**Rollback**: Revert Alembic migration, restore old model. Service code can be deleted cleanly (no dependencies yet).

## Open Questions

- Should ingredients be case-insensitive unique per product? (e.g., "tomate" vs "Tomate"?) → Decide in implementation.
- Do we need an index on `Product.category_id` for faster filtering? → Add if performance testing shows need.
- Should soft-deleted products be visible to admins by default? → Defer to admin module; ProductsService doesn't expose this yet.
