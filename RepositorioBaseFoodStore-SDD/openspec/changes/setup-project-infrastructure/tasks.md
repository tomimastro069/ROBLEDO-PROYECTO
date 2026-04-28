## 1. Backend Initialization

- [x] 1.1 Set up virtual environment and install FastAPI dependencies.
- [x] 1.2 Create project structure with layered architecture (Router → Service → UoW → Repository).
- [x] 1.3 Configure Alembic for PostgreSQL migrations.
- [ ] 1.4 Integrate SQLModel for ORM and database schema.
- [ ] 1.5 Implement JWT-based authentication (access/refresh tokens).
- [ ] 1.6 Set up RBAC roles and enforce in service-layer entry points.

## 2. Frontend Initialization

- [ ] 2.1 Bootstrap frontend with Vite, React, and TypeScript.
- [ ] 2.2 Configure Tailwind CSS for styling and Recharts for metrics.
- [ ] 2.3 Set up TanStack Query for server-side state management.
- [ ] 2.4 Initialize Zustand for client-side state (e.g., cart management).
- [ ] 2.5 Implement Axios client with JWT interception.

## 3. Payment Gateway Integration

- [ ] 3.1 Add MercadoPago SDK to backend for IPN webhook handling.
- [ ] 3.2 Implement payment state machine for order lifecycle management.
- [ ] 3.3 Test MercadoPago sandbox environment for E2E validation.

## 4. CI/CD Setup

- [ ] 4.1 Configure GitHub Actions for backend pytest workflows.
- [ ] 4.2 Add Vitest workflows for frontend testing.
- [ ] 4.3 Automate schema validation and Alembic migration runs.
- [ ] 4.4 Set up .env management and security scans.

## 5. Priority tasks for the first sprint

 Backend
 B1 · Crear estructura feature-first (9 módulos: auth, usuarios, categorias, productos, pedidos, pagos, admin, direcciones, shared)
 B2 · Configurar FastAPI con CORS y rate limiting
 B3 · Instalar y configurar SQLModel + Alembic
 B4 · Crear seed.py con datos iniciales
 B5 · Implementar BaseRepository[T] genérico
 B6 · Implementar Unit of Work con context manager
 B7 · Implementar get_current_user() y require_role()
🟡 Frontend
 F1 · Bootstrap Vite + React + TypeScript strict
 F2 · Crear estructura FSD (6 capas: app, pages, widgets, features, entities, shared)
 F3 · Configurar Tailwind CSS + React Router
 F4 · Configurar TanStack Query + Axios con interceptors JWT
 F5 · Crear authStore con Zustand
 F6 · Crear cartStore con Zustand
 F7 · Crear paymentStore con Zustand
 F8 · Crear uiStore con Zustand
 F9 · Implementar ProtectedRoute HOC por rol
