## ADDED Requirements

### Requirement: User and Role Modeling
The system SHALL store Users and Roles using SQLModel, defining a one-to-many relationship where one Role can belong to multiple Users.

#### Scenario: User Role assignment
- **WHEN** a User record is created or updated in the database
- **THEN** it MUST reference a valid Role ID
- **THEN** the relationship MUST be loaded correctly from either side

### Requirement: Category Hierarchies with Soft Delete Audit Trail
The system SHALL allow Categories to be nested hierarchically by self-referencing `parent_id` and support soft-delete (audit trail) via `deleted_at` timestamp.

#### Scenario: Sub-category persistence
- **WHEN** a Category is defined with a `parent_id`
- **THEN** the database MUST enforce the foreign key constraint referencing the same Category table
- **THEN** retrieving a parent category MUST allow accessing its child categories
- **THEN** soft-deleted categories (with `deleted_at IS NOT NULL`) MUST be excluded from all queries by default

#### Scenario: Category soft-delete audit trail
- **WHEN** a Category is deleted via DELETE endpoint
- **THEN** it MUST NOT be physically removed from the database
- **THEN** it MUST be marked with a `deleted_at` timestamp for audit purposes
- **THEN** the Category.deleted_at field MUST be of type Optional[datetime]
- **THEN** querying categories MUST filter out records where deleted_at IS NOT NULL

### Requirement: Product Modeling with Decimal Precision
The system SHALL store Products with standard fields (name, description, price, stock) and relationships to Categories, Ingredients, and Allergens. Product prices MUST use Decimal type for financial precision (not float).

#### Scenario: Product with multiple ingredients and Decimal price
- **WHEN** a Product is saved
- **THEN** its associated Ingredients and Allergens MUST be properly linked and queryable
- **THEN** the price field MUST be of type Decimal with precision(10, scale=2)
- **THEN** PostgreSQL MUST represent price as NUMERIC(10,2) for storage

### Requirement: Order State Machine
The system SHALL model Orders with an Enum for state transitions (e.g. PENDING, PAID, PREPARING, SHIPPED, DELIVERED) and a many-to-many relationship with Products via an OrderItem table.

#### Scenario: Order items and status
- **WHEN** an Order is created
- **THEN** it MUST be initialized in the PENDING state
- **THEN** it MUST include associated OrderItems that record the product ID, quantity, and historical price

