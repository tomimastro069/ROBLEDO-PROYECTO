## ADDED Requirements

### Requirement: Alembic configuration uses Pydantic
The system MUST configure the Alembic database URL dynamically via the application's Pydantic settings rather than a static `alembic.ini` file, ensuring a single source of truth for database connections.

#### Scenario: Running Alembic migrations
- **WHEN** the `alembic upgrade head` command is executed
- **THEN** the migrations connect to the PostgreSQL database defined by `.env` variables via `app.core.config.settings`

### Requirement: Idempotent database seeder
The system MUST provide a script to safely seed initial system data (such as default roles and an admin user) that can be run repeatedly without duplicating records or throwing constraint errors.

#### Scenario: Running the seeder script multiple times
- **WHEN** the seeder script is executed on a database that already contains the seed data
- **THEN** the script completes successfully without duplicating records or crashing due to UNIQUE constraints

### Requirement: Cleanup of legacy scaffolding
The system MUST NOT contain legacy scaffolding files (`backend/models.py` and `backend/seed.py`) that conflict with the domain models.

#### Scenario: Application startup and imports
- **WHEN** the application runs
- **THEN** all domain models are loaded exclusively from `backend/app/core/models.py` without ambiguity