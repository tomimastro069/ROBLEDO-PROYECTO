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

### Requirement: UoW Dependency Injection
The system MUST provide a FastAPI dependency that yields a Unit of Work context manager, guaranteeing that routers do not directly manage database sessions.

#### Scenario: Endpoint database access
- **WHEN** a router endpoint defines `uow: AppUnitOfWork = Depends(get_uow)`
- **THEN** FastAPI successfully injects the AppUnitOfWork instance ready to be used in a `with` block