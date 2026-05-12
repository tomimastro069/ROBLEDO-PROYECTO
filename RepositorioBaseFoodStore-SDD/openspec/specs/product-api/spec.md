# Specification: Product API

## Purpose
Expose the Product Catalog functionalities via REST HTTP endpoints, allowing clients to browse, search, and manage products and their associated metadata (ingredients, allergens).

## Requirements

### R1: Paginated Product Listing
The system SHALL expose `GET /products` returning a paginated list of active products (not soft-deleted), supporting optional filters by `category_id` and `search`.

#### Scenario: List products without filters
- **WHEN** `GET /products` is called without query parameters
- **THEN** returns HTTP 200 with `{ items: [...], total: int, limit: int, offset: int }` with up to 20 products

#### Scenario: Listar productos paginados
- **WHEN** `GET /products?skip=20&limit=10` es llamado
- **THEN** retorna HTTP 200 con la segunda página de 10 productos y `total` con el conteo global

#### Scenario: Filtrar por categoría
- **WHEN** `GET /products?category_id=3` es llamado
- **THEN** retorna HTTP 200 con solo los productos cuyo `category_id` es 3, paginados

#### Scenario: Buscar productos por nombre
- **WHEN** `GET /products?search=tomate` es llamado
- **THEN** retorna HTTP 200 con productos cuyo nombre contenga "tomate" (case-insensitive), paginados

#### Scenario: Lista vacía
- **WHEN** `GET /products?category_id=999` es llamado y no existen productos en esa categoría
- **THEN** retorna HTTP 200 con `{ items: [], total: 0, limit: 20, offset: 0 }`

### Requirement: Obtener producto por ID
El sistema SHALL exponer `GET /products/{id}` retornando el producto con sus ingredientes y alérgenos anidados, o 404 si no existe o está soft-deleted.

#### Scenario: Producto encontrado
- **WHEN** `GET /products/123` es llamado y el producto con id=123 existe y no está soft-deleted
- **THEN** retorna HTTP 200 con `{ id, name, description, price, stock, category_id, ingredients: [...], allergens: [...] }`

#### Scenario: Producto no encontrado
- **WHEN** `GET /products/9999` es llamado y no existe ningún producto con ese ID
- **THEN** retorna HTTP 404 con `{ "detail": "Product not found" }`

#### Scenario: Producto soft-deleted
- **WHEN** `GET /products/123` es llamado y el producto con id=123 tiene `deleted_at` no nulo
- **THEN** retorna HTTP 404 con `{ "detail": "Product not found" }`

### Requirement: Crear producto
El sistema SHALL exponer `POST /products` para crear un nuevo producto. Solo roles Admin y Gestor Stock pueden crear productos.

#### Scenario: Crear producto como Admin
- **WHEN** `POST /products` es llamado con token JWT de rol Admin y body `{ name, description, price, stock, category_id }`
- **THEN** retorna HTTP 201 con el producto creado incluyendo su `id` generado

#### Scenario: Crear producto sin autenticación
- **WHEN** `POST /products` es llamado sin header `Authorization`
- **THEN** retorna HTTP 401 con `{ "detail": "Not authenticated" }`

#### Scenario: Crear producto como Cliente
- **WHEN** `POST /products` es llamado con token JWT de rol Cliente
- **THEN** retorna HTTP 403 con `{ "detail": "Not enough permissions" }`

#### Scenario: Crear producto con datos inválidos
- **WHEN** `POST /products` es llamado con token Admin y `price: -5`
- **THEN** retorna HTTP 422 con errores de validación de Pydantic

### Requirement: Actualizar producto
El sistema SHALL exponer `PUT /products/{id}` para actualizar campos de un producto existente. Solo roles Admin y Gestor Stock pueden actualizar.

#### Scenario: Actualizar producto como Gestor Stock
- **WHEN** `PUT /products/123` es llamado con token JWT de rol Gestor Stock y body `{ "price": "15.50" }`
- **THEN** retorna HTTP 200 con el producto actualizado reflejando el nuevo precio

#### Scenario: Actualizar producto inexistente
- **WHEN** `PUT /products/9999` es llamado con token Admin
- **THEN** retorna HTTP 404 con `{ "detail": "Product not found" }`

#### Scenario: Actualizar sin permisos
- **WHEN** `PUT /products/123` es llamado con token de rol Cliente
- **THEN** retorna HTTP 403 con `{ "detail": "Not enough permissions" }`

### Requirement: Soft-delete de producto
El sistema SHALL exponer `DELETE /products/{id}` para hacer soft-delete de un producto. Solo Admin y Gestor Stock pueden eliminar.

#### Scenario: Soft-delete como Admin
- **WHEN** `DELETE /products/123` es llamado con token Admin
- **THEN** retorna HTTP 204 sin cuerpo y el producto queda con `deleted_at` no nulo en la DB

#### Scenario: Soft-delete de producto inexistente
- **WHEN** `DELETE /products/9999` es llamado con token Admin
- **THEN** retorna HTTP 404 con `{ "detail": "Product not found" }`

#### Scenario: Soft-delete sin permisos
- **WHEN** `DELETE /products/123` es llamado con token de rol Gestor Pedidos
- **THEN** retorna HTTP 403 con `{ "detail": "Not enough permissions" }`

### Requirement: Gestión de ingredientes via HTTP
El sistema SHALL exponer sub-endpoints `GET/POST/DELETE /products/{id}/ingredients` para listar, agregar y eliminar ingredientes de un producto.

#### Scenario: Listar ingredientes de un producto
- **WHEN** `GET /products/123/ingredients` es llamado (sin auth)
- **THEN** retorna HTTP 200 con lista de `{ id, product_id, name }` del producto 123

#### Scenario: Agregar ingrediente como Admin
- **WHEN** `POST /products/123/ingredients` es llamado con token Admin y `{ "name": "tomate" }`
- **THEN** retorna HTTP 201 con el ingrediente creado `{ id, product_id, name }`

#### Scenario: Eliminar ingrediente como Gestor Stock
- **WHEN** `DELETE /products/123/ingredients/456` es llamado con token Gestor Stock
- **THEN** retorna HTTP 204 y el ingrediente con id=456 es eliminado de la DB

#### Scenario: Ingrediente de producto inexistente
- **WHEN** `POST /products/9999/ingredients` es llamado con token Admin
- **THEN** retorna HTTP 404 con `{ "detail": "Product not found" }`

### Requirement: Gestión de alérgenos via HTTP
El sistema SHALL exponer sub-endpoints `GET/POST/DELETE /products/{id}/allergens` para listar, agregar y eliminar alérgenos de un producto.

#### Scenario: Listar alérgenos de un producto
- **WHEN** `GET /products/123/allergens` es llamado (sin auth)
- **THEN** retorna HTTP 200 con lista de `{ id, product_id, name }` del producto 123

#### Scenario: Agregar alérgeno como Admin
- **WHEN** `POST /products/123/allergens` es llamado con token Admin y `{ "name": "gluten" }`
- **THEN** retorna HTTP 201 con el alérgeno creado `{ id, product_id, name }`

#### Scenario: Eliminar alérgeno como Gestor Stock
- **WHEN** `DELETE /products/123/allergens/789` es llamado con token Gestor Stock
- **THEN** retorna HTTP 204 y el alérgeno con id=789 es eliminado de la DB

### Requirement: RBAC enforcement en products-api
El sistema SHALL aplicar control de acceso basado en roles en todos los endpoints de escritura del catálogo de productos.

#### Scenario: Roles con acceso de escritura
- **WHEN** un endpoint de escritura (`POST`, `PUT`, `DELETE`) es llamado con token de rol Admin
- **THEN** la operación es autorizada y procesada

#### Scenario: Roles con acceso de escritura — Gestor Stock
- **WHEN** un endpoint de escritura es llamado con token de rol Gestor Stock
- **THEN** la operación es autorizada y procesada

#### Scenario: Roles sin acceso de escritura
- **WHEN** un endpoint de escritura es llamado con token de rol Cliente o Gestor Pedidos
- **THEN** retorna HTTP 403 con `{ "detail": "Not enough permissions" }`
