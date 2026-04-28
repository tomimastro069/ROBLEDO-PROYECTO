## 1. Backend Initialization

- [x] 1.1 Set up virtual environment and install FastAPI dependencies.
- [x] 1.2 Create project structure with layered architecture (Router → Service → UoW → Repository).
- [x] 1.3 Configure Alembic for PostgreSQL migrations.
- [x] 1.4 Integrate SQLModel for ORM and database schema.
- [x] 1.5 Implement JWT-based authentication (access/refresh tokens).
- [x] 1.6 Set up RBAC roles and enforce in service-layer entry points.

## 2. Frontend Initialization

- [x] 2.1 Bootstrap frontend with Vite, React, and TypeScript.
- [x] 2.2 Configure Tailwind CSS for styling and Recharts for metrics.
- [x] 2.3 Set up TanStack Query for server-side state management.
- [x] 2.4 Initialize Zustand for client-side state (e.g., cart management).
- [x] 2.5 Implement Axios client with JWT interception.

## 3. Payment Gateway Integration

- [ ] 3.1 Add MercadoPago SDK to backend for IPN webhook handling.
- [ ] 3.2 Implement payment state machine for order lifecycle management.
- [ ] 3.3 Test MercadoPago sandbox environment for end-to-end validation.

## 4. CI/CD Setup

- [ ] 4.1 Configure GitHub Actions for backend pytest workflows.
- [ ] 4.2 Add Vitest workflows for frontend testing.
- [ ] 4.3 Automate schema validation and Alembic migration runs.
- [ ] 4.4 Set up .env management and security scans.

## 5. Priority tasks for the first sprint (Sprint 0 - COMPLETO ✅)

- [x] B1 Create feature-first structure (9 modules)
- [x] B2 Configure FastAPI with CORS and rate limiting
- [x] B3 Install and configure SQLModel + Alembic
- [x] B4 Create seed.py with initial data
- [x] B5 Implement generic BaseRepository[T]
- [x] B6 Implement Unit of Work with context manager
- [x] B7 Implement get_current_user() and require_role()

- [x] F1 Bootstrap Vite + React + TypeScript strict
- [x] F2 Create FSD structure (6 layers: app, pages, widgets, features, entities, shared)
- [x] F3 Configure Tailwind CSS + React Router
- [x] F4 Configure TanStack Query + Axios with JWT interceptors
- [x] F5 Create authStore with Zustand
- [x] F6 Create cartStore with Zustand
- [x] F7 Create paymentStore with Zustand
- [x] F8 Create uiStore with Zustand
- [x] F9 Implement ProtectedRoute HOC by role
