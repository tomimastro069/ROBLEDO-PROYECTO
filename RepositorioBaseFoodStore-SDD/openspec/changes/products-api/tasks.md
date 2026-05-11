## 1. Limpieza previa

- [x] 1.1 Buscar todos los imports de `backend/app/schemas/products.py` en el codebase y actualizarlos a `backend/products/schemas.py` (capa Router)
- [x] 1.2 Eliminar `backend/app/schemas/products.py` (schema legacy con `price: float`)
- [x] 1.3 Verificar `ProductsService.read_all(skip, limit)` — confirmar que la paginación es DB-level y no slicing en memoria; corregir si es slicing

## 2. Tests TDD — escribir antes de implementar

- [x] 2.1 Crear `backend/tests/products/test_products_router.py` con fixtures de TestClient, usuario Admin, usuario Gestor Stock, usuario Cliente, y seed de productos/categorías en DB de test
- [x] 2.2 Escribir tests para `GET /products`: sin filtros (200 + estructura paginada), con `?skip=&limit=`, con `?category_id=`, con `?search=`, categoría sin productos (200 lista vacía)
- [x] 2.3 Escribir tests para `GET /products/{id}`: producto existente (200 con ingredientes/alérgenos), id inexistente (404), producto soft-deleted (404)
- [x] 2.4 Escribir tests para `POST /products`: como Admin (201), sin auth (401), como Cliente (403), payload inválido (422)
- [x] 2.5 Escribir tests para `PUT /products/{id}`: como Gestor Stock actualiza precio (200), id inexistente (404), como Cliente (403)
- [x] 2.6 Escribir tests para `DELETE /products/{id}`: como Admin (204 + verifica soft-delete en DB), id inexistente (404), como Gestor Pedidos (403)
- [x] 2.7 Escribir tests para `/products/{id}/ingredients`: GET lista (200), POST como Admin (201), DELETE como Gestor Stock (204), producto inexistente (404)
- [x] 2.8 Escribir tests para `/products/{id}/allergens`: GET lista (200), POST como Admin (201), DELETE como Gestor Stock (204)
- [x] 2.9 Ejecutar `pytest backend/tests/products/test_products_router.py` — confirmar que todos los tests FALLAN (red phase de TDD)

## 3. Implementación — Router

- [x] 3.1 Crear `backend/products/router.py` con endpoints CRUD del catálogo (`GET /products`, `GET /products/{id}`, `POST /products`, `PUT /products/{id}`, `DELETE /products/{id}`) usando `get_products_service` y RBAC con `get_current_user`
- [x] 3.2 Agregar sub-endpoints de ingredientes: `GET /products/{id}/ingredients`, `POST /products/{id}/ingredients`, `DELETE /products/{id}/ingredients/{ingredient_id}`
- [x] 3.3 Agregar sub-endpoints de alérgenos: `GET /products/{id}/allergens`, `POST /products/{id}/allergens`, `DELETE /products/{id}/allergens/{allergen_id}`
- [x] 3.4 Registrar `products_router` en `backend/main.py` con `prefix="/products"` y `tags=["products"]`

## 4. Verificación

- [x] 4.1 Ejecutar `pytest backend/tests/products/test_products_router.py` — todos los tests deben pasar (green phase)
- [x] 4.2 Ejecutar suite completa `pytest backend/tests` — sin regresiones en otros módulos
- [ ] 4.3 Levantar servidor (`uvicorn backend.main:app --reload`) y verificar `/docs` que refleja los endpoints de productos con sus esquemas y badges de autenticación
