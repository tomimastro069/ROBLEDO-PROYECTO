## ADDED Requirements

### Requirement: Centralized PostgreSQL UoW
The system MUST instantiate the Unit of Work using the PostgreSQL engine defined in `app.core.database` without overriding it with hardcoded SQLite configurations.

#### Scenario: Running transactions
- **WHEN** a service enters a `with AppUnitOfWork() as uow:` block
- **THEN** it executes queries against the PostgreSQL database configured via `.env`

### Requirement: Concrete Repositories
The system MUST provide concrete repositories that extend `BaseRepository` to encapsulate domain-specific queries without leaking SQL alchemy statements into the business logic.

#### Scenario: Querying user by email
- **WHEN** the service calls `uow.users.get_by_email("test@test.com")`
- **THEN** the concrete `UserRepository` executes the specific SQLModel select query and returns the user object or `None`

### Requirement: Soft-Delete Filtering in Repositories
Repositories for entities with soft-delete support (e.g., Category) MUST override query methods to automatically filter soft-deleted records (where deleted_at IS NULL).

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
