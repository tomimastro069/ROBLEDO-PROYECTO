# Análisis Gap — Historias de Usuario vs Roadmap vs Código

> **Fecha**: 2026-05-12  
> **Rama**: main  
> **Total de historias de usuario**: 77 (US-000 a US-076) en 18 épicas

El proyecto tiene **77 historias de usuario** en 18 épicas (Sprint 0 → Sprint 8). El roadmap marca 21 changes, de los cuales **20 están implementados** (change 21 `mercadopago-integration` sin [X]).

---

## ✅ Lo que está completo

| Módulo | Estado |
|---|---|
| Sprint 0 — Infraestructura (US-000 a US-000e, US-068, US-074) | ✅ Completo |
| Auth backend (US-001 a US-006, US-073) | ✅ Completo |
| Categorías (US-007 a US-010) | ✅ Completo |
| Productos (US-015 a US-022) | ✅ Completo |
| Pedidos — servicio y API (US-035 a US-044) | ✅ Completo |
| Webhook MercadoPago (US-046 parcial) | ✅ Existe |
| Cart store Zustand (US-029 a US-034 — store) | ✅ Existe |
| Frontend base: stores, axios, router, ProtectedRoute | ✅ Completo |

---

## ❌ Lo que FALTA — Backend

### 1. EPIC 04 — Ingredientes y Alérgenos (US-011 a US-014) — Alta prioridad

No existe módulo `ingredientes/`. Los modelos están en BD pero no hay endpoints. Sin esto, la asociación producto-ingrediente no es operable desde la API.

- Falta: `POST /api/v1/ingredientes`
- Falta: `GET /api/v1/ingredientes`
- Falta: `PUT /api/v1/ingredientes/:id`
- Falta: `DELETE /api/v1/ingredientes/:id`

### 2. EPIC 07 — Direcciones de Entrega (US-024 a US-028) — Alta prioridad

No existe módulo `direcciones/`. Los pedidos necesitan una dirección para crearse con snapshot.

- Falta: `POST /api/v1/direcciones`
- Falta: `GET /api/v1/direcciones`
- Falta: `PUT /api/v1/direcciones/:id`
- Falta: `DELETE /api/v1/direcciones/:id`
- Falta: `PATCH /api/v1/direcciones/:id/predeterminada`

### 3. EPIC 06 — Perfil del Cliente (US-061, 062, 063) — Media prioridad

No existen endpoints de perfil del usuario autenticado.

- Falta: `GET /api/v1/perfil`
- Falta: `PUT /api/v1/perfil`
- Falta: `PUT /api/v1/perfil/password`

### 4. EPIC 11 — Pagos MercadoPago incompleto (US-045, US-047, US-048)

Solo existe el webhook (US-046). Falta:

- `POST /api/v1/pagos/crear` — iniciar pago con MercadoPago (US-045)
- `GET /api/v1/pedidos/:id/pago` — consultar estado de pago (US-047)
- Lógica de reintento de pago rechazado (US-048)

### 5. EPIC 15 — Administración de Usuarios (US-053 a US-055) — Alta prioridad

No existe módulo `admin/` con gestión de usuarios.

- Falta: `GET /api/v1/admin/usuarios`
- Falta: `PUT /api/v1/admin/usuarios/:id`
- Falta: `PATCH /api/v1/admin/usuarios/:id/estado`

### 6. EPIC 17 — Métricas y Dashboard (US-056 a US-059) — Media prioridad

No existen endpoints de métricas.

- Falta: `GET /api/v1/admin/metricas/resumen`
- Falta: `GET /api/v1/admin/metricas/ventas`
- Falta: `GET /api/v1/admin/metricas/productos-top`
- Falta: `GET /api/v1/admin/metricas/pedidos-por-estado`

### 7. EPIC 18 — Configuración del Sistema (US-060) — Baja prioridad

No implementado.

---

## ❌ Lo que FALTA — Frontend

El frontend tiene la base (stores, router, auth hooks, cart features, layouts) pero le faltan todas las páginas funcionales:

| Página / Feature | US | Estado |
|---|---|---|
| RegisterPage | US-001 | ❌ Solo existe LoginPage |
| CatalogPage (productos, filtros, búsqueda) | US-018, US-023 | ❌ |
| ProductDetailPage + exclusión de ingredientes | US-019, US-030 | ❌ |
| DireccionesPage (CRUD) | US-024 a US-028 | ❌ |
| CheckoutPage (flujo completo) | US-035, US-069 | ❌ |
| OrdersPage / OrderDetailPage (cliente) | US-049, US-050 | ❌ |
| Páginas de retorno de pago (success/failure/pending) | US-072 | ❌ |
| Navegación con menú por rol | US-075 | ❌ |
| ProfilePage | US-061, US-062, US-063 | ❌ |
| Panel Admin — Usuarios, Métricas, Dashboard | US-053 a US-059 | ❌ |
| Panel Gestor Pedidos (gestión FSM) | US-051, US-052 | ❌ |

---

## ⚠️ Problemas técnicos detectados

### Inconsistencia de rutas en `main.py`

Los routers están registrados con prefijos diferentes, lo cual rompe la convención `/api/v1/` definida en la spec:

| Router | Prefijo actual | Prefijo correcto |
|---|---|---|
| orders | `/api/v1/orders` | ✅ |
| auth | `/auth` | ❌ → `/api/v1/auth` |
| categories | `/categories` | ❌ → `/api/v1/categories` |
| products | `/products` | ❌ → `/api/v1/products` |

### CORS abierto

`allow_origins=["*"]` en producción es un problema de seguridad. US-000a requería explícitamente leer los orígenes desde variable de entorno `CORS_ORIGINS`.

---

## Resumen por sprint

| Sprint | Contenido | Estado |
|---|---|---|
| Sprint 0 | Infraestructura | ✅ Completo |
| Sprint 1 | Auth backend | ✅ Completo |
| Sprint 2 | Categorías | ✅ Completo |
| Sprint 3 | Productos + Perfil | ⚠️ Productos ✅ — Perfil ❌ |
| Sprint 4 | Direcciones + Carrito | ⚠️ Cart store ✅ — Direcciones ❌ |
| Sprint 5 | Checkout + Pedidos backend | ⚠️ Backend ✅ — Frontend ❌ |
| Sprint 6 | Pagos completo + FSM | ⚠️ FSM ✅ — Pagos parcial ❌ |
| Sprint 7 | Visualización pedidos | ❌ Frontend completo faltante |
| Sprint 8 | Admin + Métricas | ❌ No iniciado |

---

## Orden de ataque recomendado

Lo más crítico para tener el flujo mínimo funcional (cliente puede comprar):

1. **Backend**: módulo `ingredientes/` (desbloquea asociación con productos)
2. **Backend**: módulo `direcciones/` (desbloquea creación de pedidos real)
3. **Backend**: endpoints de pagos crear/consultar (completa integración MercadoPago)
4. **Backend**: corregir prefijos de rutas a `/api/v1/`
5. **Frontend**: CatalogPage + ProductDetailPage
6. **Frontend**: CheckoutPage + flujo de pedido completo
7. **Frontend**: OrdersPage + páginas de retorno de pago
8. **Backend + Frontend**: admin usuarios + métricas
