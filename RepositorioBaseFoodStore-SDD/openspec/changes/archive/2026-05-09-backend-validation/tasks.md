## 1. Setup inicial de DTOs

- [x] 1.1 Crear directorio `backend/app/schemas/` y el archivo `__init__.py`.
- [x] 1.2 Crear esquema base `base.py` si hubiese tipos comunes.
- [x] 1.3 Crear esquema `users.py` (ej. UserCreate, UserRead, UserUpdate) con validaciones de email y password.

## 2. Modelado de DTOs adicionales

- [x] 2.1 Crear esquema `products.py` (ej. ProductCreate con precios > 0 y stock >= 0).
- [x] 2.2 Crear esquema `categories.py` (ej. CategoryCreate).
- [x] 2.3 Crear esquema `orders.py` (ej. OrderCreate, OrderItemCreate).

## 3. Integración en Endpoints y Mapeo

- [x] 3.1 Actualizar las firmas de rutas en `backend/app/api/` para recibir los DTOs como body (en lugar de recibir SQLModels o `dict` sueltos).
- [x] 3.2 Asegurar que el paso de DTO a ORM (antes de llamar al UnitOfWork) instancie correctamente el SQLModel.

## 4. Finalización y Progreso

- [x] 4.1 Actualizar el archivo `RepositorioBaseFoodStore-SDD/docs/map/map.md` marcando el change 9 (`backend-validation`) con `[X]`.