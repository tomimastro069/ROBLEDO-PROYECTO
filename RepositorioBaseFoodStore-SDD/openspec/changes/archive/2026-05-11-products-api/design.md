## Context

El Change #15 (`products-service`) entregó la capa de servicio y repositorio del catálogo de productos: `ProductsService`, `ProductsRepository`, `ProductIngredientRepository`, `ProductAllergenRepository`, y los schemas Pydantic en `backend/products/schemas.py` con `Decimal` para precios. Sin embargo, `backend/main.py` no monta ningún router de productos, por lo que la API REST no existe aún.

Existe también un set de schemas legacy en `backend/app/schemas/products.py` que define `price: float`, lo que genera inconsistencia con los schemas canónicos. Este diseño también resuelve esa deuda técnica.

## Goals / Non-Goals

**Goals:**
- Exponer el catálogo de productos vía REST (`/products`) siguiendo el patrón `categories-api`.
- Implementar RBAC: lectura pública, escritura solo para Admin y Gestor Stock.
- Proporcionar paginación DB-level (no in-memory slicing) para listados y búsquedas.
- Eliminar `backend/app/schemas/products.py` (float legacy) y unificar en `backend/products/schemas.py`.
- Gestión de ingredientes y alérgenos como sub-recursos de producto.

**Non-Goals:**
- Frontend / consumo desde React (change posterior).
- Integración con MercadoPago o pedidos.
- Endpoints de stock management avanzado (ajuste de inventario por pedido está en orders-api).
- Migración de base de datos (el schema de DB ya existe y es correcto).

## Decisions

### Decision: Feature-First Router

**Elección**: Crear `backend/products/router.py` dentro del slice `products/`, inyectando `get_products_service`.  
**Alternativas**: Router global en `backend/app/api/`.  
**Rationale**: Consistente con `categories/router.py`. Mantiene cohesión por feature. Más fácil de testear y modificar de forma aislada.

### Decision: Lectura pública, escritura con RBAC

**Elección**:
- `GET /products`, `GET /products/{id}`, `GET /products/{id}/ingredients`, `GET /products/{id}/allergens` → sin autenticación requerida.
- `POST`, `PUT`, `DELETE` → requieren `Authorization: Bearer <token>` + rol Admin o Gestor Stock.

**Alternativas**: Todos los endpoints requieren auth.  
**Rationale**: Los clientes navegan el catálogo sin login. Las operaciones de escritura son administrativas. Alinea con dominio e-commerce del proyecto.

### Decision: Schemas canónicos — eliminar legacy

**Elección**: Usar `backend/products/schemas.py` como única fuente de verdad. Eliminar `backend/app/schemas/products.py`.  
**Alternativas**: Mantener ambos y crear un adaptador.  
**Rationale**: Dos schemas con tipos distintos (`Decimal` vs `float`) para el mismo dato es una deuda activa. Eliminar el legacy es limpio y evita bugs futuros de precisión de precio.

### Decision: Paginación DB-level

**Elección**: Usar los métodos paginados ya existentes en `ProductsRepository` (`get_by_category`, `search_by_name`). Para `GET /products` general, el repository ya implementa `get_all()` filtrado; añadir `read_all(skip, limit)` al servicio si no existe.  
**Alternativas**: Paginar en la capa de servicio con slicing en memoria.  
**Rationale**: El slicing in-memory escala mal. Los repositorios ya tienen la infraestructura de paginación SQL.

### Decision: Sub-recursos para ingredientes y alérgenos

**Elección**: `GET/POST/DELETE /products/{id}/ingredients` y `GET/POST/DELETE /products/{id}/allergens`.  
**Alternativas**: Incluir ingredientes/alérgenos siempre en el payload del producto.  
**Rationale**: Mantiene los payloads básicos livianos. El endpoint `GET /products/{id}` retorna el producto con campos básicos; si el cliente necesita los ingredientes hace una segunda llamada. El schema `ProductWithIngredientsAndAllergens` existe para respuestas compuestas si se prefiere en el futuro.

### Decision: Error handling — HTTPException (no RFC7807 aún)

**Elección**: Usar `HTTPException` de FastAPI directo, igual que `categories-api`.  
**Alternativas**: Pasar a `DomainException` (RFC7807 via `backend/app/core/exceptions.py`).  
**Rationale**: La migración a RFC7807 es un change transversal que no debe bloquearse en products-api. Mantener consistencia con el módulo de categorías ya implementado.

## Risks / Trade-offs

| Riesgo | Probabilidad | Mitigación |
|--------|-------------|------------|
| Tests existentes importan `backend/app/schemas/products.py` | Media | Buscar todos los imports antes de eliminar; actualizar a `backend/products/schemas.py` |
| `ProductRead` no incluye `deleted_at`/`created_at` — endpoints podrían necesitarlos | Baja | Verificar campos en `ProductRead` al implementar; ampliar si es necesario |
| `ProductsService.read_all` pagina con slicing interno | Alta | Verificar implementación y corregir a paginación real en el servicio antes de exponer en router |
| RBAC: roles mal definidos en tokens de prueba | Media | Revisar fixtures de tests de auth para usar roles correctos en tests de integración |

## Migration Plan

1. Corregir `backend/app/schemas/products.py` eliminando el archivo tras confirmar que ningún módulo activo lo importa.
2. Registrar `products_router` en `backend/main.py` (no requiere migración de DB).
3. Rollback: remover import + `app.include_router(...)` de `main.py`; el router es additive.

## Open Questions

- ¿El endpoint `GET /products/{id}` debe retornar `ProductRead` (básico) o `ProductWithIngredientsAndAllergens` (compuesto)? → Decisión: retornar compuesto para simplificar el cliente.
