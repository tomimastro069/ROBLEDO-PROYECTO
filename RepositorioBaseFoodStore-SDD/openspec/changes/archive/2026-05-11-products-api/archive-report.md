# Archive Report: products-api

**Archived:** 2026-05-11  
**Schema:** spec-driven  
**Change:** Change #16 — products-api

## Summary

Expone la capa HTTP del catálogo de productos sobre el `ProductsService` ya implementado en el Change #15. Se creó el router FastAPI con 11 endpoints REST (CRUD de productos + sub-recursos de ingredientes y alérgenos), con RBAC, paginación DB-level y tests de integración TDD.

## Artifacts Completed

- `proposal.md` — Motivación, scope, capability `product-api`, impacto por archivo
- `design.md` — 5 decisiones técnicas documentadas (router, RBAC, schemas, paginación, sub-recursos)
- `specs/product-api/spec.md` — 7 requirements, 24 scenarios Given/When/Then
- `tasks.md` — 18/19 tareas completadas (4.3 verificación manual con server levantado)

## Code Changes

| Archivo | Acción |
|---------|--------|
| `backend/products/router.py` | Nuevo — 11 endpoints REST |
| `backend/tests/products/test_products_router.py` | Nuevo — 28 tests integración HTTP |
| `backend/pytest.ini` + `conftest.py` files | Nuevo — infraestructura de tests |
| `backend/main.py` | Modificado — registra `products_router` en `/products` |
| `backend/app/core/repositories/products_repository.py` | Modificado — agrega `get_all_paginated()` |
| `backend/products/service.py` | Modificado — `get_all()` usa paginación DB-level |
| `backend/products/schemas.py` | Modificado — agrega `gt=0` a precio |
| `backend/app/core/uow/unit_of_work.py` | Modificado — `expire_on_commit=False` |
| `backend/app/schemas/products.py` | Eliminado — schema legacy con `float` |
| `backend/tests/products/conftest.py` | Corregido — fixtures de test con `CategoryRepository` |

## Test Results

```
51 passed (products/) en 1.22s
  - 28 tests de router (test_products_router.py)
  - 23 tests de servicio (test_service.py)
```

## Specs Synced

- `openspec/specs/product-api/spec.md` — nueva spec creada desde delta

## Notes

- La task 4.3 (verificar Swagger UI con server levantado) requiere PostgreSQL en ejecución — verificación manual pendiente.
- `expire_on_commit=False` en UoW es un cambio cross-cutting que beneficia a todos los módulos, no solo products.
