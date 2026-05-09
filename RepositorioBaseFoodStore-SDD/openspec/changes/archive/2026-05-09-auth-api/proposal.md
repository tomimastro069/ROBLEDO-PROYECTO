# Proposal: Auth API

## Intent

Expose the real authentication business logic (`auth-service`) via REST API endpoints, completely removing the temporary hardcoded mock implementation from Sprint 0 to establish a secure and functional authentication boundary.

## Scope

### In Scope
- Creation of `backend/auth/router.py` defining REST endpoints for `/register`, `/login` (or `/token`), `/refresh`, and `/me`.
- Injection of `AuthService` into the new router using FastAPI's `Depends`.
- Deletion of the legacy mock file `backend/app/core/auth.py`.
- Re-wiring of the main FastAPI application (`backend/main.py`) to mount the new router.

### Out of Scope
- Frontend integration (handled in `auth-frontend`).
- Third-party OAuth (Google, Facebook) integrations.

## Approach

Use **Approach 1 (Dedicated router with dependency injection)**:
Create a cohesive `router.py` inside the `backend/auth/` feature slice. The router will depend on `get_auth_service` and delegate the heavy lifting to the `AuthService`. The old mock router in `app/core/auth.py` will be safely deleted, and `main.py` will be updated to point to the new feature module.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `backend/auth/router.py` | New | Dedicated API router for auth endpoints |
| `backend/app/core/auth.py` | Removed | Delete legacy mock endpoints and static `users_db` |
| `backend/main.py` | Modified | Update router import and registration |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Dependency issues after removing `core/auth.py` | Low | Verify no other files import from `core/auth.py` before deletion. |
| API Contract changes | Medium | Ensure new `/token` endpoint is compatible with `OAuth2PasswordRequestForm` standard for Swagger UI. |

## Rollback Plan

Delete `backend/auth/router.py`, restore `backend/app/core/auth.py` from git history, and revert `backend/main.py` to point back to the core auth router.

## Dependencies

- `auth-service` (Completed in Change 10).

## Success Criteria

- [ ] New auth router successfully handles real registration and login using DB.
- [ ] Legacy `backend/app/core/auth.py` is entirely removed.
- [ ] `/docs` Swagger UI works seamlessly with the new login flow.
