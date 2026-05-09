# Design: Auth Service

## Technical Approach

We will implement an `AuthService` class that encapsulates the business rules of authentication. To maintain the Feature-First and clean architecture established in Sprint 0, this service will be completely decoupled from direct SQLModel or DB session calls. Instead, it will rely entirely on the injected `UnitOfWork` to orchestrate transactions and utilize `backend/auth/utils.py` for cryptography.

## Architecture Decisions

### Decision: Password Hashing Library

**Choice**: Use `passlib` with `bcrypt`.
**Alternatives considered**: Built-in `hashlib` (too manual, error-prone), `argon2` (slightly heavier).
**Rationale**: `passlib[bcrypt]` is the standard, battle-tested approach in the FastAPI ecosystem and balances security with performance.

### Decision: Database Abstraction in Service

**Choice**: Inject `UnitOfWork` into `AuthService`.
**Alternatives considered**: Injecting individual repositories or raw DB sessions.
**Rationale**: `UnitOfWork` guarantees atomic transactions (especially if registration expands in the future) and prevents the service from knowing about database internals.

## Data Flow

    [API Route] ──(UserCreate)──→ [AuthService] 
                                        │ (hashes password using utils)
                                        │
                                        └──(User dict)──→ [UnitOfWork] ──→ [BaseRepository (users)] ──→ [DB]

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `backend/auth/schemas.py` | Create | Pydantic models: `UserCreate`, `UserLogin`, `Token` |
| `backend/auth/utils.py` | Create | Functions: `get_password_hash`, `verify_password`, `create_access_token`, `create_refresh_token` |
| `backend/auth/service.py` | Create | Class `AuthService` with methods `register`, `login`, `refresh` |

## Interfaces / Contracts

```python
# backend/auth/schemas.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

# backend/auth/service.py
class AuthService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        
    def register(self, user_in: UserCreate) -> User: ...
    def login(self, email: str, password: str) -> Token: ...
    def refresh(self, refresh_token: str) -> Token: ...
```

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | `auth/utils.py` | Test that hashes differ from plain text, validation works, and JWTs contain correct claims. |
| Unit | `AuthService` | Mock `UnitOfWork` to test business logic isolation (registration prevents duplicates, login fails on bad password). |

## Migration / Rollout

No migration required. The `users` table already exists from Sprint 0.

## Open Questions

- None.
