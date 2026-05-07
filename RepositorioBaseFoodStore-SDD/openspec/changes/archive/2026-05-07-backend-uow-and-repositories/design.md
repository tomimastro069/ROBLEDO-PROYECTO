## Context

Currently, the `backend/uow` and `backend/shared` directories exist loosely in the root directory. They provide the foundational generic repository and UoW logic, but `unit_of_work.py` contains hardcoded SQLite engine configurations that override our PostgreSQL connection. We need to restructure these into the `app/core` boundary, wire the database correctly, and implement concrete repositories for our first domain entities so services can safely orchestrate database transactions.

## Goals / Non-Goals

**Goals:**
- Move `backend/shared` and `backend/uow` into `backend/app/core/`.
- Refactor `UnitOfWork` to consume the global `engine` exported by `backend/app/core/database.py` instead of re-instantiating a SQLite engine.
- Establish `AppUnitOfWork`, an application-specific subclass of UoW that instantiates concrete repositories inside the `__enter__` block.
- Create initial concrete repositories: `UserRepository(BaseRepository[User])` and `RoleRepository(BaseRepository[Role])`.
- Expose a FastAPI dependency `get_uow()` for dependency injection in route handlers.

**Non-Goals:**
- Implementing business logic services (Services will wrap the UoW in the next steps).
- Implementing all domain repositories at once (We will only scaffold the base architecture and User/Role repos initially).

## Decisions

1. **Folder Consolidation:**
   - **Decision**: Move the UoW and generic repository code inside `app/core/`.
   - **Rationale**: Core architectural components should live inside the `app` boundary, specifically `core`, protecting the outer layer from structural leaks. 

2. **Concrete Repository Pattern:**
   - **Decision**: Create a `repositories` folder inside `app/core/` for base and concrete repositories.
   - **Rationale**: While some architectures place repositories inside feature modules (e.g. `app/users/repository.py`), centralizing them or attaching them directly to the `AppUnitOfWork` simplifies the transactional boundary. We will create specific repository classes that extend `BaseRepository` to add specific queries (like `get_by_email`).

3. **UoW Instantiation via Dependency Injection:**
   - **Decision**: Create a `def get_uow()` function in `app.core.uow` that returns a fresh instance of `AppUnitOfWork`.
   - **Rationale**: FastAPI's `Depends(get_uow)` is the cleanest way to provide a localized transaction context to a route or service without passing the session directly.

## Risks / Trade-offs

- **Risk: Import cycles.** Moving files might break existing imports if other files (like seeder) already imported them.
  - **Mitigation**: Perform a full search-and-replace across the codebase for imports pointing to `shared.base_repository` or `uow.unit_of_work` during the refactoring task.
- **Trade-off: Centralized vs Decentralized UoW.** 
  - Having a single `AppUnitOfWork` that instantiates all repositories could grow large. However, it ensures absolute transactional integrity across boundaries (e.g., creating an Order and updating Product Stock in the same transaction). We will accept the large class size in favor of strict atomic guarantees.