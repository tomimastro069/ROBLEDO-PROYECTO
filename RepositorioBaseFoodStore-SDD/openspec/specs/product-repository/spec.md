# Specification: Product Repository

## Purpose
Define the data access requirements for products, ingredients, and allergens, ensuring consistent CRUD operations and specialized domain queries.

## Requirements

### R1: Product Base CRUD
The ProductsRepository SHALL extend BaseRepository and provide all standard CRUD operations.

#### Scenario: Get product by ID
- **WHEN** ProductsRepository.get_by_id(product_id=123) is called
- **THEN** returns the Product with id=123, or None if not found.

#### Scenario: Get all products (excluding soft-deleted)
- **WHEN** ProductsRepository.get_all() is called
- **THEN** returns all products where deleted_at IS NULL.

#### Scenario: Add product to database
- **WHEN** ProductsRepository.add(product_entity) is called
- **THEN** the product is persisted and returned with an assigned ID.

#### Scenario: Update existing product
- **WHEN** ProductsRepository.update(product_entity) is called with modified fields
- **THEN** the product is merged into the session and flushed with updated values

#### Scenario: Delete product from database
- **WHEN** ProductsRepository.delete(product_entity) is called
- **THEN** the product is removed from the session and flushed (physical delete at DB level, NOT soft delete)

### Requirement: Specialized Product Queries
The ProductsRepository SHALL provide domain-specific queries for filtering and pagination.

#### Scenario: Get products by category with pagination
- **WHEN** ProductsRepository.get_by_category(category_id=5, skip=0, limit=20) is called
- **THEN** returns tuple(items: list[Product], total: int) with products from category 5, excluding soft-deleted, with pagination

#### Scenario: Search products by name
- **WHEN** ProductsRepository.search_by_name(query="tomate", skip=0, limit=10) is called
- **THEN** returns tuple(items: list[Product], total: int) with products matching ILIKE(query), excluding soft-deleted

#### Scenario: Search returns pagination info
- **WHEN** ProductsRepository.search_by_name("tomate", skip=10, limit=5) is called and there are 200 matching products
- **THEN** returns tuple(items: list[5 products], total: 200) so frontend can build pagination controls

### Requirement: Stock Validation Query
The ProductsRepository SHALL support stock availability checks.

#### Scenario: Validate stock level
- **WHEN** ProductsRepository.validate_stock_available(product_id=123, quantity=5) is called and product.stock >= 5
- **THEN** returns True

#### Scenario: Insufficient stock returns false
- **WHEN** ProductsRepository.validate_stock_available(product_id=123, quantity=10) is called and product.stock = 5
- **THEN** returns False

### Requirement: Soft Delete Filtering in All Queries
The ProductsRepository SHALL automatically exclude soft-deleted products (deleted_at IS NOT NULL) from all queries.

#### Scenario: Soft-deleted product excluded from get_by_category
- **WHEN** a product is soft-deleted (deleted_at IS NOT NULL) and get_by_category() is called
- **THEN** the soft-deleted product does NOT appear in results

#### Scenario: Soft-deleted product excluded from search
- **WHEN** a product is soft-deleted and search_by_name() is called with a matching name
- **THEN** the soft-deleted product does NOT appear in results

### Requirement: Related Entity Repositories
The system SHALL provide ProductIngredientRepository and ProductAllergenRepository for managing ingredient and allergen data.

#### Scenario: Add product ingredient via ProductIngredientRepository
- **WHEN** ProductIngredientRepository.add(ProductIngredient(product_id=123, name="tomate", is_allergen=False)) is called
- **THEN** the ingredient is persisted and linked to the product

#### Scenario: Get ingredients for a product
- **WHEN** ProductIngredientRepository.get_by_product(product_id=123) is called
- **THEN** returns list[ProductIngredient] with all ingredients for that product

#### Scenario: Remove ingredient via ProductIngredientRepository
- **WHEN** ProductIngredientRepository.delete(ingredient_entity) is called
- **THEN** the ingredient link is removed from the database
