# Tasks: Auth API

## Phase 1: Create Router

- [x] 1.1 Create `backend/auth/router.py`.
- [x] 1.2 Import `APIRouter`, schemas (`UserCreate`, `UserLogin`, `Token`), and dependencies (`get_auth_service`, `get_current_user`).
- [x] 1.3 Implement `POST /register` injecting `AuthService`, returning HTTP 201.
- [x] 1.4 Implement `POST /login` receiving `UserLogin` JSON, returning `Token` payload.
- [x] 1.5 Implement `POST /refresh` receiving `refresh_token`, returning new `Token`.
- [x] 1.6 Implement `GET /me` injecting `get_current_user`, returning `TokenData`.

## Phase 2: System Wiring and Cleanup

- [x] 2.1 Edit `backend/main.py`: Replace `from app.core.auth import router as auth_router` with `from auth.router import router as auth_router`.
- [x] 2.2 Delete `backend/app/core/auth.py`.
- [x] 2.3 Verify application starts correctly without import errors.
