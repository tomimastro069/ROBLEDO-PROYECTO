# Sprint 0 — Implementation Tasks

> Ordered by execution blocks. A block only starts when the previous one is complete.
> Backend tasks were completed on 2026-04-27.

---

## BACKEND — Bloque único (✅ Completo)

- [x] B1 · Estructura feature-first (9 módulos: auth, users, categories, products, orders, payments, admin, addresses, shared)
- [x] B2 · FastAPI + CORS + rate limiting (slowapi)
- [x] B3 · SQLModel + Alembic configurados
- [x] B4 · `seed.py` con datos iniciales
- [x] B5 · `BaseRepository[T]` genérico → `backend/shared/base_repository.py`
- [x] B6 · Unit of Work con context manager → `backend/uow/unit_of_work.py`
- [x] B7 · `get_current_user()` + `require_role()` → `backend/auth/dependencies.py`

---

## FRONTEND — Bloque 1: Fundación (✅ Completo)

- [x] F1 · Bootstrap Vite + React + TypeScript strict
- [x] F2 · Crear estructura FSD (6 capas)

---

## FRONTEND — Bloque 2: Infraestructura (✅ Completo)

- [x] F3 · Tailwind CSS + React Router
- [x] F4 · TanStack Query + Axios con interceptors JWT

---

## FRONTEND — Bloque 3: Stores (✅ Completo)

- [x] F5 · `authStore` (Zustand)
- [x] F6 · `cartStore` (Zustand)
- [x] F7 · `paymentStore` (Zustand)
- [x] F8 · `uiStore` (Zustand)

---

## FRONTEND — Bloque 4: Composición (✅ Completo)

- [x] F9 · `ProtectedRoute` HOC por rol

---

## Criterios de salida del Sprint 0

- [ ] Backend corriendo en `:8000` con docs en `/docs`
- [ ] Frontend corriendo en `:5173`
- [ ] BD inicializada con seed
- [x] Scaffold completo: `feat(setup): scaffold backend FFA + frontend FSD + UoW + stores`
