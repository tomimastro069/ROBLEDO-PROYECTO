## Why

El Change #15 (`products-service`) implementó la lógica de negocio del catálogo de productos con su repositorio, servicio y schemas, pero no expone ningún endpoint HTTP. El sistema no tiene forma de consultar, crear, actualizar ni eliminar productos vía API. Este change cierra esa brecha montando el router FastAPI del módulo `productos`, habilitando el CRUD completo del catálogo para clientes y administradores.

## What Changes

- **New**: `backend/products/router.py` — router FastAPI con endpoints CRUD de productos, búsqueda paginada, y gestión de ingredientes y alérgenos.
- **New**: `backend/tests/products/test_products_router.py` — tests de integración de la capa HTTP (Strict TDD: tests primero).
- **Modified**: `backend/main.py` — registrar el router de productos en `/products`.
- **Modified**: `backend/products/schemas.py` — agregar campos faltantes al schema de respuesta (`deleted_at`, `created_at`) y schema de respuesta de lista paginada si no existe.
- **Removed**: `backend/app/schemas/products.py` — eliminar schemas legacy con `price: float` que generan inconsistencia con `Decimal`.

## Capabilities

### New Capabilities

- `product-api`: Endpoints REST HTTP para el catálogo de productos — CRUD (create, read, update, soft-delete), listado paginado, búsqueda por nombre, filtro por categoría, y sub-endpoints para gestión de ingredientes y alérgenos por producto. Incluye RBAC: lectura pública (o autenticada), escrituras solo para roles Admin y Gestor Stock.

### Modified Capabilities

<!-- Sin cambios de requerimientos en specs existentes -->

## Impact

| Área | Impacto | Descripción |
|------|---------|-------------|
| `backend/products/router.py` | Nuevo | Router con 10+ endpoints para el catálogo |
| `backend/tests/products/test_products_router.py` | Nuevo | Tests de integración HTTP (TDD) |
| `backend/main.py` | Modificado | Registrar `products_router` en prefix `/products` |
| `backend/products/schemas.py` | Modificado | Alinear schemas de respuesta con campos reales del modelo |
| `backend/app/schemas/products.py` | Eliminado | Schemas legacy con `float` reemplazados por `backend/products/schemas.py` |
| `backend/auth/dependencies.py` | Dependencia | `get_current_user` y verificación de roles |
| `backend/products/dependencies.py` | Dependencia | `get_products_service` ya existe |
