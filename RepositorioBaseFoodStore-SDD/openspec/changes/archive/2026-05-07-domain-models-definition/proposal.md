## Why

The backend architecture requires a foundational data model to persist e-commerce data (Users, Categories, Products, Orders, Payments, etc.) into the PostgreSQL database. Creating these domain models using SQLModel is a prerequisite for all other backend features, as the Service and Repository layers depend on them.

## What Changes

- Create the base SQLModel classes for the entire food store domain.
- Define models for: Users (with roles), Categories (hierarchical), Products (with ingredients and allergens), Orders (with state transitions), Payments, and Addresses.
- Establish relationships (one-to-many, many-to-many) between the models using SQLModel relationship attributes.
- Generate initial Alembic migrations to reflect these domain models in the database.

## Capabilities

### New Capabilities
- `domain-models`: Definition of the core database schema and SQLModel entities for the e-commerce system.

### Modified Capabilities
- 

## Impact

- **Database**: Creates the foundational tables in PostgreSQL via Alembic migrations.
- **Backend Architecture**: Provides the `Model` layer for all future modules (auth, usuarios, categorias, productos, pedidos, pagos, direcciones).
- **Rollback Plan**: Alembic downgrade to base revision if the initial migration fails.
