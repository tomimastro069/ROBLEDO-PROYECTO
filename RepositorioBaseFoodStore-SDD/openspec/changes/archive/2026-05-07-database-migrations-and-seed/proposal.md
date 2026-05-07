## Why

The backend currently has legacy SQLite configurations and leftover scaffolding files (`models.py`, `seed.py` in the root). To move forward with the real PostgreSQL infrastructure, we need to correctly configure Alembic to read `DATABASE_URL` dynamically from Pydantic (`config.py`), remove the legacy SQLite references, and create a truly idempotent database seeder to establish our core roles and initial state without duplication errors.

## What Changes

- Update Alembic's `env.py` to inject the database URL from `app.core.config.settings.DATABASE_URL` instead of reading the hardcoded SQLite URL from `alembic.ini`.
- Remove legacy SQLite configuration in `alembic.ini`.
- Delete leftover scaffolding files: `backend/models.py` and `backend/seed.py`.
- Create a new idempotent `backend/app/core/seeder.py` (or similar script) using a "Find or Create" pattern to populate initial domain data (e.g., Roles like 'Admin' and 'Customer').
- **BREAKING**: Migrations will now target the PostgreSQL database defined in `.env`.

## Capabilities

### New Capabilities
- `database-infrastructure`: Establishes the core PostgreSQL migration pipeline and idempotent database seeding mechanism for application startup and deployments.

### Modified Capabilities
- None.

## Impact

- **Database**: Switches from SQLite to PostgreSQL.
- **Migrations**: Alembic execution will now depend entirely on `app.core.config` and the `.env` file, establishing a Single Source of Truth for configuration.
- **Bootstrapping**: Introduces a reliable seed mechanism that can be run repeatedly in deployment pipelines without side effects.
