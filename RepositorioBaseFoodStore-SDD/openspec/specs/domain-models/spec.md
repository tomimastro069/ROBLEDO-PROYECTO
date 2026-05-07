## ADDED Requirements

### Requirement: User and Role Modeling
The system SHALL store Users and Roles using SQLModel, defining a one-to-many relationship where one Role can belong to multiple Users.

#### Scenario: User Role assignment
- **WHEN** a User record is created or updated in the database
- **THEN** it MUST reference a valid Role ID
- **THEN** the relationship MUST be loaded correctly from either side

### Requirement: Category Hierarchies
The system SHALL allow Categories to be nested hierarchically by self-referencing `parent_id`.

#### Scenario: Sub-category persistence
- **WHEN** a Category is defined with a `parent_id`
- **THEN** the database MUST enforce the foreign key constraint referencing the same Category table
- **THEN** retrieving a parent category MUST allow accessing its child categories

### Requirement: Product Modeling
The system SHALL store Products with standard fields (name, description, price, stock) and relationships to Categories, Ingredients, and Allergens.

#### Scenario: Product with multiple ingredients
- **WHEN** a Product is saved
- **THEN** its associated Ingredients and Allergens MUST be properly linked and queryable

### Requirement: Order State Machine
The system SHALL model Orders with an Enum for state transitions (e.g. PENDING, PAID, PREPARING, SHIPPED, DELIVERED) and a many-to-many relationship with Products via an OrderItem table.

#### Scenario: Order items and status
- **WHEN** an Order is created
- **THEN** it MUST be initialized in the PENDING state
- **THEN** it MUST include associated OrderItems that record the product ID, quantity, and historical price
