# Mapa de Progreso - FoodStore Project

## Sprint 0: Infrastructure Setup (Feature-First + FSD)
**Estado Actual:** Finalizado 🚀

### Backend (Feature-First Architecture)
- [x] **B1: Estructura base de módulos**
- [x] **B2: FastAPI, CORS & Rate Limiting**
- [x] **B3: SQLModel & Alembic integration**
- [x] **B4: Seed system**
- [x] **B5: BaseRepository genérico**
- [x] **B6: Unit of Work pattern**
- [x] **B7: Auth Dependencies (JWT + Roles)**

### Frontend (Feature-Sliced Design)
- [x] **F1: Vite + TS Strict setup**
- [x] **F2: FSD Directory Structure**
- [x] **F3: Tailwind & React Router setup**
- [x] **F4: TanStack Query & Axios Client**
- [x] **F5: Auth Store (Zustand + Persist)**
- [x] **F6: Cart Store (Zustand)**
- [x] **F7: Payment Store (Zustand)**
- [x] **F8: UI Store (Zustand)**
- [x] **F9: ProtectedRoute HOC**

---

## Próximo Sprint: Sprint 1 (Core Features)
- [ ] **US-001: Autenticación & Registro**
- [ ] **US-002: Catálogo de Productos**
- [ ] **US-003: Gestión de Carrito**

---

## Archivos Clave Creados
- `backend/shared/base_repository.py`
- `backend/uow/unit_of_work.py`
- `backend/auth/dependencies.py`
- `frontend/src/app/router.tsx`
- `frontend/src/app/providers.tsx`
- `frontend/src/shared/api/axios.ts`
- `frontend/src/entities/auth/model/authStore.ts`
- `frontend/src/shared/ui/ProtectedRoute.tsx`
