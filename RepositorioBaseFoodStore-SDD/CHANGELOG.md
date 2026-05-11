# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-05-11

### Added - Change #15: Products Service

- **Product Model**: Added `Decimal` type for precise price handling (NUMERIC(10,2) in PostgreSQL)
- **Soft-Delete Support**: Added `deleted_at: Optional[datetime]` field to Product model for auditable soft-deletion
- **ProductsRepository**: 
  - Implemented with soft-delete filtering in all queries (get_by_id, get_all, get_by_category, search_by_name)
  - Added specialized queries: get_by_category(), search_by_name(), validate_stock_available()
  - Added stock management methods: decrease_stock(), increase_stock()
- **ProductIngredientRepository**: CRUD operations for product ingredients (product-specific, not global)
- **ProductAllergenRepository**: CRUD operations for product allergens (product-specific, not global)
- **ProductsService**: 
  - 5 CRUD methods: create(), get_by_id(), get_all(), update(), delete()
  - 6 ingredient management methods: add_ingredient(), get_ingredients(), remove_ingredient()
  - 6 allergen management methods: add_allergen(), get_allergens(), remove_allergen()
  - 2 stock management methods: validate_stock_available(), decrease_stock(), increase_stock()
- **Pydantic Schemas**: 7 schemas with Decimal support and validators
- **Dependency Injection**: get_products_service() for FastAPI integration
- **Integration Tests**: 23 test cases covering CRUD, ingredients, allergens, stock management, and specialized queries
- **Alembic Migrations**: 
  - Migration 001: Update Product.price from FLOAT to NUMERIC(10,2)
  - Migration 002: Add Product.deleted_at for soft-delete support

### Changed

- **AppUnitOfWork**: Registered ProductsRepository, ProductIngredientRepository, ProductAllergenRepository

### Technical Details

- Decimal type requires `from_attributes=True` in Pydantic ConfigDict for ORM→schema conversion
- All repositories respect soft-delete pattern: queries filter `deleted_at IS NULL`
- Service layer coordinates 3 repositories within UnitOfWork for transaction atomicity
- Stock operations use explicit methods (decrease_stock, increase_stock) instead of direct updates for auditability
