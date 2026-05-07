## Context

The backend scaffolding generated a few legacy files (`backend/models.py`, `backend/seed.py`) and configured Alembic to use SQLite by default in `alembic.ini`. The domain models are correctly defined inside `app/core/models.py` using `SQLModel`. The goal now is to properly connect Alembic to PostgreSQL using Pydantic configurations (`app.core.config`), clean up the legacy files, and create a solid, idempotent seeder to populate foundational data (Roles, Admin User) without duplication.

## Goals / Non-Goals

**Goals:**
- Configure Alembic to retrieve the database URL securely from the Pydantic config (`app.core.config.settings.DATABASE_URL`).
- Remove legacy SQLite configuration and scaffolding files.
- Implement an idempotent database seeder (`app.core.seeder` or similar) that uses "Find or Create" patterns.
- Ensure the database initialization can run safely on every deployment without duplicating records.

**Non-Goals:**
- Modifying the domain models themselves (they are already correctly defined in `app/core/models.py`).
- Setting up the Docker Compose or Dockerfile (this was handled in `dockerization-setup`).
- Implementing the UoW or Repositories patterns in this step (they follow in step 7 of the map).

## Decisions

1. **Alembic Configuration via Pydantic:**
   - **Decision**: Update `backend/migrations/env.py` to import `app.core.config.settings` and overwrite `sqlalchemy.url` dynamically.
   - **Rationale**: Avoids maintaining the URL in multiple places (`alembic.ini` and `.env`). Establishes `config.py` as the Single Source of Truth.
   - **Alternative**: Modifying `alembic.ini` directly via bash scripts or environment variables substitution tools. Rejected because Python-based configuration via `env.py` is safer, type-checked, and idiomatic for FastAPI.

2. **Idempotent Seeder Implementation:**
   - **Decision**: Create an asynchronous script `backend/app/core/seeder.py` that uses SQLModel queries to check for existence before inserting records. 
   - **Rationale**: A simple `session.add()` will crash or duplicate data on subsequent runs. By querying first (e.g., `select(Role).where(Role.name == "Admin")`), the script becomes safe to execute automatically during the CI/CD pipeline or container startup.

3. **Legacy File Deletion:**
   - **Decision**: Completely delete `backend/models.py` and `backend/seed.py`.
   - **Rationale**: These were scaffolding artifacts. Their existence creates confusion and duplication with `app/core/models.py`.

## Risks / Trade-offs

- **Risk: Migration Mismatch**: If there are existing SQLite migrations generated, they might fail or conflict when applied to PostgreSQL.
  - **Mitigation**: Delete the existing `backend/migrations/versions` files and regenerate the initial migration from scratch specifically targeting PostgreSQL.
- **Risk: Seeder Performance**: "Find or Create" is slower than bulk inserts.
  - **Mitigation**: The seeder only inserts a handful of foundational records (Roles, initial Admin, maybe categories). The performance hit is negligible at startup.