# Tasks: Auth Service

## Phase 1: Foundation (Schemas & Utils)

- [x] 1.1 Create `backend/auth/schemas.py` and define `UserCreate`, `UserLogin`, and `Token` models.
- [x] 1.2 Create `backend/auth/utils.py` and implement `get_password_hash` and `verify_password` using `passlib`.
- [x] 1.3 In `backend/auth/utils.py`, implement `create_access_token` and `create_refresh_token` using `python-jose` (ensure secrets load from config).

## Phase 2: Core Implementation (Service)

- [x] 2.1 Create `backend/auth/service.py` and define the `AuthService` class injecting `UnitOfWork`.
- [x] 2.2 Implement `AuthService.register(user_in: UserCreate)`: hash password, check email uniqueness using `self.uow.users.get_by_email`, save, and commit.
- [x] 2.3 Implement `AuthService.login(email, password)`: retrieve user, verify password, and generate tokens.
- [x] 2.4 Implement `AuthService.refresh(refresh_token)`: decode token, extract sub/email, retrieve user, and issue new tokens.

## Phase 3: Wiring (Dependency Injection)

- [x] 3.1 In `backend/auth/dependencies.py` (existing), add a dependency `get_auth_service(uow: UnitOfWork = Depends(get_uow))` that returns an instance of `AuthService`.
