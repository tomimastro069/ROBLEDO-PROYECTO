# Proposal: Auth Service (Business Logic)

## Intent

Implement the core authentication business logic (`auth-service`) utilizing the `UnitOfWork` and `BaseRepository` established in Sprint 0, isolating the database access from the service layer to ensure a clean, testable architecture.

## Scope

### In Scope
- Creation of `AuthService` class injecting `UnitOfWork`.
- Implementation of `register`, `login`, and `refresh` business logic.
- Pydantic models for authentication requests and responses (`UserCreate`, `UserLogin`, `Token`).
- Password hashing and verification utilities.

### Out of Scope
- Implementation of API endpoints (REST routes) - this belongs to `auth-api`.
- Frontend authentication integration - this belongs to `auth-frontend`.

## Approach

Follow Approach 1 (Centralized Service with Injected Unit of Work):
1. **Models/Schemas:** Define Pydantic schemas in `schemas.py` for input/output validation.
2. **Utils:** Implement `passlib` based password hashing in `utils.py`.
3. **Service Layer:** Build `AuthService` in `service.py`, using `uow.users` repository for persistence and transactional boundaries.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `backend/auth/schemas.py` | New | Pydantic schemas for auth |
| `backend/auth/utils.py` | New | Hashing and JWT utility functions |
| `backend/auth/service.py` | New | Central `AuthService` class with UoW |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Secrets hardcoded in code | Low | Enforce loading JWT secrets from `.env` via `config.py` |
| Hashing vulnerabilities | Low | Use `bcrypt` via `passlib` for password hashing |

## Rollback Plan

Delete the newly created files (`backend/auth/schemas.py`, `backend/auth/utils.py`, `backend/auth/service.py`) as they do not affect existing routing or database schemas yet.

## Dependencies

- Existing `UnitOfWork` and `BaseRepository` implementations.
- `passlib`, `bcrypt`, and `python-jose` packages in `requirements.txt`.

## Success Criteria

- [ ] `AuthService` successfully hashes passwords and persists new users via UoW.
- [ ] `AuthService` correctly validates credentials and issues JWTs.
- [ ] No direct database access occurs outside the Unit of Work pattern in the service layer.
