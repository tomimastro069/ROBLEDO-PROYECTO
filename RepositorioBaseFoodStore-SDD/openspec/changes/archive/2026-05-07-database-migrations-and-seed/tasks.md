## 1. Cleanup Legacy Files

- [x] 1.1 Delete the scaffolding `backend/models.py` file to avoid collisions with the actual domain models.
- [x] 1.2 Delete the scaffolding `backend/seed.py` file to prevent accidental execution of the outdated SQLite seed logic.

## 2. Alembic Configuration

- [x] 2.1 Edit `backend/migrations/env.py` to import `app.core.config.settings` and extract the database URL.
- [x] 2.2 Modify `backend/migrations/env.py` in the `run_migrations_online` function to inject `settings.DATABASE_URL` into the Alembic config `sqlalchemy.url`.
- [x] 2.3 Verify `alembic.ini` has a dummy URL or remains untracked for real credentials, ensuring `.env` is the true source.
- [x] 2.4 Delete the existing `backend/migrations/versions` contents (if any SQLite migrations exist) to start fresh for PostgreSQL.

## 3. Database Seeder Implementation

- [x] 3.1 Create `backend/app/core/seeder.py` as an executable script.
- [x] 3.2 Implement a "Find or Create" logic inside `seeder.py` for foundational data (e.g., Roles: Admin, Cliente, Gestor Stock, Gestor Pedidos, Sistema).
- [x] 3.3 Add logic in `seeder.py` to securely seed an initial Admin user if it doesn't already exist, using the password hashing from `app.core.auth`.
- [x] 3.4 Add an entry point block (`if __name__ == "__main__":`) that establishes a database session and runs the seed functions.
