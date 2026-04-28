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