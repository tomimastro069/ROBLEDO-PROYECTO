# Design: Auth API

## Technical Approach

Create a dedicated `backend/auth/router.py` to expose the `AuthService` logic over HTTP. By using FastAPI's dependency injection (`Depends`), the router controllers will request an instance of `AuthService` dynamically and execute the business logic, mapping Pydantic schemas correctly. Finally, we wipe out the legacy code in `app/core/auth.py` to eliminate technical debt and rewire `main.py`.

## Architecture Decisions

### Decision: API Input Payload for Login

**Choice**: Use pure JSON `UserLogin` for login instead of `OAuth2PasswordRequestForm`.
**Alternatives considered**: Use `OAuth2PasswordRequestForm` (standard x-www-form-urlencoded).
**Rationale**: In modern React+Vite SPAs, JSON payloads are universally preferred and simpler to handle with Axios/Fetch than form data. Since our swagger UI (`/docs`) might break its "Authorize" button, we prioritize the Frontend app experience over Swagger UI convenience for this specific domain.

### Decision: Router Module Location

**Choice**: `backend/auth/router.py`
**Alternatives considered**: `backend/app/api/routers/auth.py`.
**Rationale**: Keeping the router next to its service, schemas, and utils inside `backend/auth/` adheres closer to the Feature-Sliced/Feature-First design pattern.

## Data Flow

    [HTTP Request] ──(JSON Body)──→ [Auth Router] 
                                         │
                                         ├── Depends(get_auth_service)
                                         │
                                         └──→ [AuthService] ──→ DB

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `backend/auth/router.py` | Create | Defines FastAPI `APIRouter` with `/register`, `/login`, `/refresh`, and `/me`. |
| `backend/app/core/auth.py` | Delete | Removes legacy code, hardcoded users, and deprecated router. |
| `backend/main.py` | Modify | Update imports to point to `auth.router` instead of `app.core.auth`. |

## Interfaces / Contracts

```python
# HTTP API Contracts

# POST /auth/register
# Request: UserCreate (JSON)
# Response 201: { "id": int, "email": str, "role_id": int }

# POST /auth/login
# Request: UserLogin (JSON)
# Response 200: Token { access_token: str, refresh_token: str, token_type: "bearer" }

# POST /auth/refresh
# Request: { "refresh_token": str } (JSON)
# Response 200: Token

# GET /auth/me
# Headers: Authorization: Bearer <token>
# Response 200: TokenData
```

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Integration | `/auth/register` | Call API with `TestClient`, assert 201 Created and DB user existence. |
| Integration | `/auth/login` | Call API with valid credentials, assert 200 OK and presence of JWT tokens. |

## Migration / Rollout

No database migration required. Requires dropping deprecated imports in `main.py` causing momentary downtime until server reloads.

## Open Questions
- None.
