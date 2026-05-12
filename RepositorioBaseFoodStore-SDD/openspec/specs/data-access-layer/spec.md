# Specification: Data Access Layer (Repository & UoW)

## Purpose
Define the patterns and requirements for data persistence, ensuring a decoupled architecture using the Repository and Unit of Work patterns.

## Requirements

### R1: Centralized Unit of Work (UoW)
The system MUST instantiate the Unit of Work using the global database engine.

#### Scenario: Running transactions
- **WHEN** a service enters a `with AppUnitOfWork() as uow:` block
- **THEN** it executes queries against the configured database.

### R2: Concrete Repositories
The system MUST provide concrete repositories that extend `BaseRepository` to encapsulate domain-specific queries.

#### Scenario: Querying entities
- **WHEN** the service calls a repository method (e.g., `uow.users.get_by_email`)
- **THEN** the concrete repository executes the specific query and returns domain objects.

### R3: Soft-Delete Filtering
Repositories for entities with soft-delete support MUST automatically filter soft-deleted records.

#### Scenario: Category queries exclude soft-deleted records
- **WHEN** a service calls `uow.categories.get_by_id(id)` or `uow.categories.get_all()`
- **THEN** the CategoryRepository MUST apply WHERE deleted_at IS NULL filter to all select statements
- **THEN** soft-deleted categories are never returned to the business logic layer
- **THEN** audit trail is maintained: soft-deleted records exist in DB with deleted_at timestamp

### Requirement: UoW Dependency Injection
The system MUST provide a FastAPI dependency that yields a Unit of Work context manager, guaranteeing that routers do not directly manage database sessions.

#### Scenario: Endpoint database access
- **WHEN** a router endpoint defines `uow: AppUnitOfWork = Depends(get_uow)`
- **THEN** FastAPI successfully injects the AppUnitOfWork instance ready to be used in a `with` block
