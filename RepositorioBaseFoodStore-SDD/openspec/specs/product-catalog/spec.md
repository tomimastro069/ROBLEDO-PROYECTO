# Specification: Product Catalog (Service)

## Purpose
Manage the core product business logic, including lifecycle (CRUD), stock validation, and metadata associations.

## Requirements

### R1: Product Lifecycle Management
The system SHALL provide Create, Read, Update, and Delete operations for products, with soft-delete semantics.

#### Scenario: Create a new product
- **WHEN** ProductsService.create() is called with valid ProductCreate data
- **THEN** a new Product is persisted with an auto-generated ID.

#### Scenario: Read a single product by ID
- **WHEN** ProductsService.read(product_id=123) is called
- **THEN** the Product is returned, or None if not found or soft-deleted.

#### Scenario: Read all products (paginated)
- **WHEN** ProductsService.read_all(skip=0, limit=20) is called
- **THEN** returns a paginated list of non-deleted products.

#### Scenario: Update a product
- **WHEN** ProductsService.update(product_id=123, data=ProductUpdate(...)) is called with new name/price/description
- **THEN** the Product is updated in the database with updated_at timestamp

#### Scenario: Soft-delete a product
- **WHEN** ProductsService.delete(product_id=123) is called
- **THEN** the Product's deleted_at is set to current timestamp (NOT removed from DB)
- **AND** subsequent queries for that product return None (or are excluded from list queries)

### Requirement: Ingredient Management
The system SHALL allow adding, removing, and retrieving ingredients associated with a product.

#### Scenario: Add ingredient to product
- **WHEN** ProductsService.add_ingredient(product_id=123, ingredient=IngredientCreate(name="tomate", is_allergen=False)) is called
- **THEN** a new ProductIngredient row is created linking the ingredient to the product

#### Scenario: Retrieve ingredients for a product
- **WHEN** ProductsService.get_ingredients(product_id=123) is called
- **THEN** returns list[ProductIngredient] containing all ingredients for that product

#### Scenario: Remove ingredient from product
- **WHEN** ProductsService.remove_ingredient(product_id=123, ingredient_id=456) is called
- **THEN** the ProductIngredient link is deleted from the database

#### Scenario: Mark ingredient as allergen
- **WHEN** ProductsService.mark_allergen(ingredient_id=456, is_allergen=True) is called
- **THEN** the ProductIngredient's is_allergen flag is updated

### Requirement: Stock Validation
The system SHALL validate that products have sufficient stock available.

#### Scenario: Validate sufficient stock
- **WHEN** ProductsService.validate_stock_available(product_id=123, quantity=5) is called and product has stock=10
- **THEN** returns True

#### Scenario: Validate insufficient stock
- **WHEN** ProductsService.validate_stock_available(product_id=123, quantity=15) is called and product has stock=10
- **THEN** returns False

#### Scenario: Validate zero stock
- **WHEN** ProductsService.validate_stock_available(product_id=123, quantity=1) is called and product has stock=0
- **THEN** returns False

### Requirement: Soft Delete Filtering
The system SHALL exclude soft-deleted products (deleted_at IS NOT NULL) from all list and search queries by default.

#### Scenario: Soft-deleted product excluded from list
- **WHEN** a product is soft-deleted and ProductsService.read_all() is called
- **THEN** the soft-deleted product does NOT appear in the results

#### Scenario: Soft-deleted product excluded from search
- **WHEN** a product is soft-deleted and ProductsService.search_by_name("tomate") is called
- **THEN** the soft-deleted product does NOT appear in results even if name matches

### Requirement: Price Precision
The system SHALL store and manage product prices as Decimal with fixed precision (e.g., 2 decimal places for currency).

#### Scenario: Price stored with correct precision
- **WHEN** ProductsService.create(data=ProductCreate(..., price=Decimal("12.99"))) is called
- **THEN** the Product.price is stored as Decimal("12.99"), not rounded or truncated

#### Scenario: Price comparison works correctly
- **WHEN** two products have prices Decimal("10.00") and Decimal("10.01")
- **THEN** comparison operators work correctly: 10.00 < 10.01 is True

### Requirement: Transaction Atomicity
The system SHALL ensure that all ProductsService operations use the Unit of Work context manager to guarantee transactional safety and atomicity.

#### Scenario: Service uses UoW context
- **WHEN** ProductsService.create() or ProductsService.update() is called
- **THEN** the operation is wrapped in a `with self.uow as uow:` context, ensuring commit or rollback

#### Scenario: Multi-step operation is atomic
- **WHEN** ProductsService performs an operation involving multiple repository calls (e.g., create product and add ingredient)
- **THEN** all changes are committed together or rolled back together (no partial success)
