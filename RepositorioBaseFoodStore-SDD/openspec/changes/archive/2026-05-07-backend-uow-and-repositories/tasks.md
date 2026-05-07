## 1. Directory Consolidation

- [x] 1.1 Move the `backend/shared/` directory to `backend/app/core/shared/`.
- [x] 1.2 Move the `backend/uow/` directory to `backend/app/core/uow/`.
- [x] 1.3 Fix the imports in `backend/app/core/shared/base_repository.py` and `backend/app/core/uow/unit_of_work.py` if they were broken by the move.

## 2. Refactor Unit of Work Engine

- [x] 2.1 Edit `backend/app/core/uow/unit_of_work.py` to remove the hardcoded SQLite URL and path resolution.
- [x] 2.2 Import the global `engine` from `app.core.database` into `unit_of_work.py` and make `get_engine()` return that PostgreSQL engine.

## 3. Concrete Repositories Implementation

- [x] 3.1 Create a new directory `backend/app/core/repositories/` with an `__init__.py` file.
- [x] 3.2 Create `backend/app/core/repositories/user_repository.py` extending `BaseRepository[User]`. Add a `get_by_email` method.
- [x] 3.3 Create `backend/app/core/repositories/role_repository.py` extending `BaseRepository[Role]`. Add a `get_by_name` method.

## 4. App Unit of Work Setup

- [x] 4.1 In `backend/app/core/uow/unit_of_work.py`, define the `AppUnitOfWork` class that inherits from `UnitOfWork`.
- [x] 4.2 Override the `__enter__` method in `AppUnitOfWork` to instantiate and attach `self.users = UserRepository(self.session)` and `self.roles = RoleRepository(self.session)`.
- [x] 4.3 Create a function `get_uow()` in `unit_of_work.py` that returns an instance of `AppUnitOfWork` to be used as a FastAPI dependency.