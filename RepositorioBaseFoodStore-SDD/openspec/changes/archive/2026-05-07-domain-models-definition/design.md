## Context

The backend application requires a data persistence layer using PostgreSQL. To interact with the database efficiently while keeping typing intact, we are using SQLModel (which combines SQLAlchemy and Pydantic). The architecture mandates feature-first modules where each domain entity requires its own model definition. These models form the core foundation upon which the Repository, Unit of Work (UoW), and Service layers will be built.

## Goals / Non-Goals

**Goals:**
- Define standard SQLModel entities for Users, Roles (RBAC), Categories, Products, Orders, Payments, and Addresses.
- Establish relationships between these models (e.g., User to Orders, Order to Order Items, Product to Categories).
- Set up the Alembic environment for tracking changes and applying the initial schema migration.

**Non-Goals:**
- Implementing the Repository or Service logic for these models.
- Implementing the HTTP Routers/Controllers.
- Setting up the frontend models.

## Decisions

**1. SQLModel for ORM:**
- *Alternative:* Raw SQLAlchemy or Tortoise ORM.
- *Decision:* SQLModel.
- *Rationale:* SQLModel natively integrates with Pydantic and FastAPI, making validation and serialization seamless across layers.

**2. Entity-Relationship Patterns:**
- **Users & Roles:** A User has a Role (e.g., Cliente, Admin). A one-to-many relationship from Role to User.
- **Hierarchical Categories:** A Category can have a `parent_id` linking to itself, enabling an N-level hierarchy.
- **Products & Ingredients/Allergens:** Text arrays or JSONB for ingredients, or separate tables if structured querying is needed. Decision: Separate `ProductIngredient` and `ProductAllergen` tables for strict normalization.
- **Orders & State Transitions:** Order entity includes a `status` enum field representing the FSM (e.g., PENDING, PAID, PREPARING, SHIPPED, DELIVERED).
- **Orders & Products:** An `OrderItem` association table handling many-to-many with additional data (quantity, price at the time of purchase).

**3. UoW Transaction Boundaries (Future-proofing):**
- While not implementing UoW now, models must be defined such that cascading deletes or updates can be managed at the SQLAlchemy session level, preserving consistency across aggregate roots like `Order`.

## Risks / Trade-offs

- **[Risk] Migration complexity with hierarchical categories.** → *Mitigation:* We will clearly define the self-referential foreign key and test the generation of the Alembic script carefully.
- **[Risk] SQLModel updates vs Pydantic v2.** → *Mitigation:* Ensure we use the latest compatible SQLModel version to avoid Pydantic v2 conflicts.
