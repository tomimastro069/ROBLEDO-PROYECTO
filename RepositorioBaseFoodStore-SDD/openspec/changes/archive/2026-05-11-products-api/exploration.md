## Exploration: products-api (Change #16) dentro de la arquitectura del proyecto

### Current State
- **Mapa de changes (docs/map/map.md)** define un flujo por capas y dependencias:
  1) scaffold monorepo → 2) backend-core → 3) docker → 4) frontend-core → 5) domain-models → 6) migrations+seed → 7) UoW+repositories → 8) error-handling → 9) validation → 10-12) auth → 13-14) categories → 15) products-service → **16) products-api (pendiente)**.
- **Backend (implementado)** sigue el patrón *Router → Service → UoW → Repository → Model* (ver `openspec/config.yaml`).
  - Entry point: `backend/main.py` monta routers de `auth` y `categories` (y webhook MercadoPago), pero **no** monta products.
  - Persistencia: SQLModel + Alembic (`backend/migrations/versions/*`).
  - UoW: `backend/app/core/uow/unit_of_work.py` registra `users/roles/categories/products/product_ingredients/product_allergens`.
  - Error handling: existe RFC7807 (`backend/app/core/exceptions.py`) pero los services actuales levantan **FastAPI HTTPException** directamente.
- **Products “Service/Repository” (Change #15) ya existe en código**:
  - Service: `backend/products/service.py`
  - DI: `backend/products/dependencies.py`
  - Schemas: `backend/products/schemas.py`
  - Repos: `backend/app/core/repositories/products_repository.py`, `product_ingredient_repository.py`, `product_allergen_repository.py`
  - Tests: `backend/tests/products/*`
- **Products API (Change #16)** en `openspec/changes/products-api/` hoy solo tiene `.openspec.yaml` (metadata). No hay `proposal.md/design.md/tasks.md/specs/` para el router.

### Affected Areas
- `backend/main.py` — debe incluir el router de productos (`app.include_router(...)`) cuando exista.
- `backend/products/` — faltaría `router.py` (HTTP layer) y alinear firmas con schemas.
- `backend/products/schemas.py` — será el contrato de request/response del products-api (o hay que unificarlo).
- `backend/app/core/repositories/products_repository.py` — ya tiene queries paginadas por category/search; falta una query paginada general si el API la necesita.
- `backend/app/schemas/products.py` — **posible duplicación/legacy**: define price como `float` (choca con `Decimal`).
- `backend/app/core/exceptions.py` — decidir si products-api usará RFC7807 (DomainException) o seguirá con HTTPException.
- `backend/auth/dependencies.py` + `backend/auth/roles.py` — RBAC para endpoints de products-api.
- `frontend/src/shared/api/axios.ts` — baseURL `/api`; requerirá endpoints consistentes y/o proxy.

### Approaches
1. **Router estilo “categories-api” (FastAPI + RBAC + schemas dedicados)**
   - Pros: consistente con `backend/categories/router.py`; fácil de mantener; RBAC explícito.
   - Cons: hoy products-service expone firmas “primitivas” (params sueltos), no recibe `ProductCreate` directo; habría que adaptar.
   - Effort: Medium

2. **Refactor previo de ProductsService para contratos “schema-first” y errores DomainException**
   - Pros: alinea con specs Openspec (Given/When/Then) y con RFC7807; reduce acoplamiento HTTP en service.
   - Cons: más cambio antes de exponer endpoints; riesgo de romper tests existentes.
   - Effort: High

### Recommendation
Implementar **Approach 1** para destrabar el flujo del mapa (Change #16 depende de #15), pero con 3 “guardrails” mínimos:
- Unificar contrato de schemas: usar `backend/products/schemas.py` como fuente única y **depreciar** `backend/app/schemas/products.py` (o migrarlo) para evitar `float` vs `Decimal`.
- Diseñar endpoints paginados que **no** carguen todo en memoria (evitar el patrón actual de `ProductsService.get_all` que pagina con slicing sobre `get_all()`).
- Definir RBAC desde el inicio: lectura pública; escrituras para `admin` y/o `gestor_stock`.

### Risks
- **Inconsistencias de modelos/schemas**: hay dos sets de schemas de producto (`backend/products/schemas.py` con Decimal vs `backend/app/schemas/products.py` con float). Esto puede generar endpoints con contratos distintos.
- **Paginación ineficiente**: `ProductsService.get_all` calcula total haciendo `len(get_all())` (carga todo). En producción escala mal.
- **Errores heterogéneos**: RFC7807 está implementado, pero services usan HTTPException → productos-api podría devolver formatos distintos a futuro.
- **Migrations**: existen varias versiones (`001_initial_schema.py`, `001_update_product_price_to_decimal.py`, `002_add_product_soft_delete.py`) con IDs/revisions potencialmente confusos; cuidado al crear nuevas migraciones.

### Ready for Proposal
Yes — pero antes, el orquestador debería pedir/definir explícitamente:
- Lista de endpoints exacta para products-api (CRUD + ingredientes/alérgenos + search + stock) y su RBAC.
- Contrato de paginación (skip/limit vs offset/limit) para mantener consistencia con categories.
- Decisión de error format: RFC7807 (DomainException) vs HTTPException estándar.
