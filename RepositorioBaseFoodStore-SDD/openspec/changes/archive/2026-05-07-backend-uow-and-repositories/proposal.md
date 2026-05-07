## Why

The backend currently has a generic Repository and Unit of Work (UoW) scaffolding that is scattered in the root directory and contains leftover SQLite hardcoding. To establish our clean, layered architecture (Router → Service → UoW → Repository), we must consolidate these files into `app/core/`, fix the database connection to use PostgreSQL natively via our configurations, and establish the concrete repositories and dependency injection patterns required by the business logic.

## What Changes

- Consolidate directory structure by moving `backend/shared/` and `backend/uow/` into `backend/app/core/`.
- **BREAKING**: Fix the UoW implementation to import the PostgreSQL engine directly from `backend/app/core/database.py`, removing the hardcoded SQLite URL.
- Create concrete repositories for our first domain entities (e.g., `UserRepository`, `ProductRepository`) extending `BaseRepository`.
- Implement a FastAPI dependency (`Depends(get_uow)`) to inject the `AppUnitOfWork` cleanly into route handlers.

## Capabilities

### New Capabilities
- `data-access-layer`: Centralizes the Unit of Work and Repository patterns, providing a transactional, PostgreSQL-backed data access foundation for all future services.

### Modified Capabilities
- None.

## Impact

- **Architecture**: Enforces the UoW pattern across all service layer boundaries. 
- **Database**: Guarantees that data operations use the correct PostgreSQL engine without SQLite ghost dependencies.
- **Dependencies**: Refactors module imports from `backend.shared` and `backend.uow` to `app.core.shared` and `app.core.uow`.
