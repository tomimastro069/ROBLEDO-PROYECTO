# Products Module Documentation

## Overview

The **products** module handles all business logic related to product management in the food store. This includes:

- **Product CRUD**: Create, read, update, delete products
- **Ingredient Management**: Add/remove ingredients to products
- **Allergen Tracking**: Track allergens for each product
- **Stock Management**: Validate and update product stock levels
- **Category Association**: Link products to categories

## Architecture

### Service Layer (`service.py`)
- `ProductsService`: Main business logic orchestrator
  - Coordinates repositories via Unit of Work
  - Validates domain rules (category existence, stock availability, no duplicates)
  - Handles Decimal price precision (no float conversions)
  - Manages transactions via UoW context manager

### Repositories (`app.core.repositories/`)
- `ProductsRepository`: Product CRUD + specialized queries
  - `get_by_category(category_id, limit, offset)` → paginated results
  - `search_by_name(query, limit, offset)` → case-insensitive substring match
  - `validate_stock_available(product_id, quantity)` → boolean
  - `decrease_stock()` / `increase_stock()` → stock management

- `ProductIngredientRepository`: Ingredient CRUD
  - `get_by_product_id(product_id)` → list of ingredients
  - `delete_by_product_id(product_id)` → cascade delete

- `ProductAllergenRepository`: Allergen CRUD
  - `get_by_product_id(product_id)` → list of allergens
  - `delete_by_product_id(product_id)` → cascade delete

### Schemas (`schemas.py`)
Pydantic models with Decimal support for JSON serialization:
- `ProductCreate`: Create payload
- `ProductRead`: Response payload
- `ProductUpdate`: Update payload (all fields optional)
- `ProductIngredientRead` / `ProductAllergenRead`: Nested data
- `PaginatedProductResponse`: Wrapper for paginated results

### Dependencies (`dependencies.py`)
- `get_products_service()`: FastAPI dependency that injects ProductsService

## Key Design Decisions

### Decimal Precision
- Product prices use `Decimal(precision=10, scale=2)` (PostgreSQL: NUMERIC)
- Ensures financial accuracy (no float precision issues)
- Pydantic schemas configured to serialize/deserialize correctly

### KISS Approach to Queries
- No full-text search (deferred to later change)
- Only basic queries: by category, substring name search
- Rationale: simpler queries, easier to optimize if needed

### Transaction Atomicity
- All operations within a service method share same Unit of Work
- Implicit commit on `with uow as uow:` exit (if no exception)
- Automatic rollback on any exception

### Ingredient/Allergen Design
- Private-per-product (not globally shared)
- Simpler schema, no cross-product dependencies
- Cascade delete handled at service layer (not DB-level)

### Soft Delete (Future Enhancement)
- Currently not implemented for Product model
- Design supports it: add `deleted_at: Optional[datetime]` to Product
- All queries already check `deleted_at IS NULL` pattern (see CategoryRepository)

## Usage Examples

### Create a Product
```python
from products.service import ProductsService
from app.core.uow.unit_of_work import AppUnitOfWork
from decimal import Decimal

uow = AppUnitOfWork()
service = ProductsService(uow)

product = service.create(
    name="Chocolate Cake",
    description="Homemade chocolate cake",
    price=Decimal("15.99"),
    stock=50,
    category_id=1
)
```

### Add Ingredients
```python
service.add_ingredient(product.id, "Flour")
service.add_ingredient(product.id, "Cocoa")
service.add_ingredient(product.id, "Eggs")

ingredients = service.get_ingredients(product.id)
```

### Track Allergens
```python
service.add_allergen(product.id, "dairy")
service.add_allergen(product.id, "eggs")

allergens = service.get_allergens(product.id)
```

### Manage Stock
```python
# Validate before placing order
if service.validate_stock_available(product.id, quantity=5):
    product = service.decrease_stock(product.id, 5)

# Restock after receiving inventory
product = service.increase_stock(product.id, 20)
```

### Search Products
```python
# By category
products, total = service.get_by_category(category_id=1, limit=50, offset=0)

# By name (case-insensitive)
results, total = service.search_by_name("chocolate", limit=10, offset=0)
```

## Testing

Run tests with:
```bash
pytest backend/tests/products/test_service.py -v
```

Test coverage includes:
- CRUD operations
- Ingredient/allergen management
- Stock validation & updates
- Category validation
- Error cases (404, 400)
- Decimal price precision
- Pagination
- Search functionality

## Integration with FastAPI

See `change #16 (products-api)` for router implementation:
- `/products` → list, create
- `/products/{id}` → get, update, delete
- `/products/{id}/ingredients` → manage ingredients
- `/products/{id}/allergens` → manage allergens
- `/products/search?q=...` → search by name
- `/products/{id}/stock` → check/update stock

## Error Handling

Common HTTP responses:
- `200 OK`: Success
- `400 Bad Request`: Invalid input (duplicate ingredient, insufficient stock)
- `404 Not Found`: Product/category not found
- `409 Conflict`: Business rule violation

## Next Steps

1. **Change #16 (products-api)**: Create FastAPI router for product endpoints
2. **Soft Delete Enhancement**: Add `deleted_at` field to Product model
3. **Full-Text Search**: Implement advanced search with FTS5 (PostgreSQL)
4. **Stock History**: Track stock movements for auditing
5. **Product Images**: Add image upload support
