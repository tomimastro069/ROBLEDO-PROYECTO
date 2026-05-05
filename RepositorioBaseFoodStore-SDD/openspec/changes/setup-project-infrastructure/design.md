## Context

The project infrastructure requires a robust setup to support the domain of e-commerce for food products. The backend will follow a layered architecture emphasizing modularity, while the frontend employs a feature-sliced design. These decisions are based on scalability, maintainability, and the diverse actors and requirements of the system (Cliente, Admin, Gestor roles).

## Goals / Non-Goals

**Goals:**
- Establish backend and frontend architectures per documented conventions.
- Ensure smooth integration with MercadoPago for payment processing.
- Create a scalable and maintainable authentication system (JWT + RBAC).
- Standardize environment configuration to streamline onboarding and CI/CD.

**Non-Goals:**
- Implementing application-specific business logic (e.g., product ordering flows).
- Frontend UI/UX fine-tuning beyond core infrastructure.
- Additional state transitions beyond e-commerce essentials.

## Decisions

### Backend Authorization
- **Decision**: Use JWT-based authentication for stateless session management. Handle role-based access control (RBAC) using service-layer checks.
- **Alternatives**: OAuth 2.0 was evaluated but set aside due to the lack of external resource servers.

### ORM Selection
- **Decision**: Employ SQLModel to leverage the Python dataclass-like syntax with ORM capabilities.
- **Alternatives**: SQLAlchemy Core/ORM was deemed less modern; Pydantic/Base was rejected for its weaker ORM.

### CI/CD Pipeline
- **Decision**: Use GitHub Actions with pytest (backend) and Vitest (frontend) for testing workflows. Add Alembic migration auto-validation.
- **Alternatives**: Jenkins was avoided due to redundancy.

## Risks / Trade-offs

[Complex JWT Expiry Handling] → Schedule refresh token lifecycle management (rotation/expiry automation).

[Database Migration Conflicts] → Use Alembic version control rigorously; adopt rollback scripts.

[Frontend State Complexity] → Clearly delineate state handled via TanStack Query vs Zustand.

[MercadoPago Integration Failure] → Utilize sandbox-environment testing pre-launch.

## Migration Plan

1. Initialize Python 3.11+ backend using FastAPI.
2. Scaffold frontend with Vite + Tailwind + TanStack Query.
3. Configure sequential Alembic migrations for PostgreSQL schema.
4. Deploy CI/CD (GitHub Actions) for backend + frontend testing.
5. Conduct thorough E2E sandbox testing of MercadoPago.

## Open Questions

- Should we optimize JWTs for embedded claims, or retain minimal payloads?
- Do we need finer-grained RBAC distinctions beyond the 5-role schema?
- How do we handle multi-language support in shared components for orders/users?

---

## Frontend Execution Strategy — Task Prioritization

Tasks are grouped into dependency-aware blocks. A block can only start when
all tasks in the previous block are complete.

### Block 1 — Foundation *(blocks everything)*

| # | Task | Reason |
|---|------|--------|
| F1 | Vite + React + TypeScript strict | Entry point — no other task can exist without this |
| F2 | FSD folder structure (6 layers) | Defines where every future file lives |

### Block 2 — Infrastructure *(depends on F1+F2, parallel)*

| # | Task | Reason |
|---|------|--------|
| F3 | Tailwind CSS + React Router | Styling system and routing — needed before any page |
| F4 | TanStack Query + Axios JWT interceptors | HTTP layer — needed before any data fetching |

### Block 3 — Stores *(depends on F1, parallel among themselves)*

| # | Task | Reason |
|---|------|--------|
| F5 | `authStore` (Zustand) | Auth state — needed for ProtectedRoute (F9) |
| F6 | `cartStore` (Zustand) | Cart state — independent of auth |
| F7 | `paymentStore` (Zustand) | Payment state — independent of auth |
| F8 | `uiStore` (Zustand) | Global UI state (modals, toasts, loading) |

### Block 4 — Composition *(depends on F3 + F5)*

| # | Task | Reason |
|---|------|--------|
| F9 | `ProtectedRoute` HOC by role | Needs router (F3) + authStore (F5) to check role |

### Dependency Tree

```
F1 → F2 → F3 ──────────────────────────┐
          └──► F4                        │
F1 → F5 ────────────────────────────────┴──► F9
     F6, F7, F8  (no downstream deps in Sprint 0)
```

### Decision: Zustand over Redux

Zustand chosen for client state because:
- Zero boilerplate vs Redux Toolkit
- Compatible with TanStack Query (server state stays in Query, UI state in Zustand)
- `authStore` exposes `user`, `token`, `setAuth()`, `clearAuth()` — enough for Sprint 0

TanStack Query owns **all server state** (products, orders, categories).
Zustand owns **client-only state** (cart items, payment intent, UI flags).

### Backend Refinements
- **Lifespan Pattern**: Migrated from deprecated `on_event` to `lifespan` context manager.
- **Middleware State**: Explicitly bound `SlowAPI` limiter to `app.state.limiter`.
- **Strict Endpoint Typing**: Enforced `fastapi.Request` typing on rate-limited endpoints.