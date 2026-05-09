# Design: categories-service

## Technical Approach

El módulo de categorías se adherirá al patrón Feature-Sliced Design en el backend, ubicándose en `backend/categories/` junto con sus schemas y lógica de servicio. El acceso a la base de datos se aislará en `CategoryRepository` dentro del core y se orquestará utilizando el `AppUnitOfWork`.

## Architecture Decisions

### Decision: Ubicación del Repository

**Choice**: Ubicar `CategoryRepository` en `app/core/repositories/` y registrarlo en `AppUnitOfWork`.
**Rationale**: Mantiene el patrón centralizado de UoW, permitiendo que cualquier servicio obtenga el repositorio mediante la sesión transaccional compartida del UoW.

### Decision: Categorías Jerárquicas en get_tree

**Choice**: Devolver solo categorías raíz (`parent_id == None`) y confiar en el ORM (SQLModel/SQLAlchemy) para poblar anidadamente las subcategorías.
**Alternatives considered**: Construir el árbol en memoria o usar consultas CTE recursivas.
**Rationale**: Para el tamaño esperado del catálogo (unos pocos niveles de anidamiento), la relación ORM con `lazy="joined"` o acceso directo es suficiente y reduce la complejidad del código.

### Decision: Regla de Eliminación (Soft vs Hard)

**Choice**: Eliminación física (Hard Delete), pero con bloqueo lógico si la categoría tiene `subcategories`.
**Alternatives considered**: Implementar un campo `is_deleted` (Soft delete) o eliminación en cascada.
**Rationale**: Evita la pérdida accidental de ramas enteras del catálogo. Obliga al administrador a reasignar explícitamente productos y subcategorías antes de eliminar un nodo padre.

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `backend/app/core/repositories/category_repository.py` | Create | Extiende `BaseRepository`, añade queries de jerarquía. |
| `backend/app/core/uow/unit_of_work.py` | Modify | Instancia y expone `CategoryRepository`. |
| `backend/categories/schemas.py` | Create | Define DTOs (Pydantic) para validación IO. |
| `backend/categories/service.py` | Create | Implementa reglas de negocio y orquestación UoW. |

## Interfaces / Contracts

```python
# categories/schemas.py
class CategoryCreate(CategoryBase)
class CategoryUpdate(BaseModel)
class CategoryWithChildren(CategoryRead) # incluye subcategories: List

# categories/service.py
class CategoriesService:
    def create(self, data: CategoryCreate) -> Category: ...
    def get_all(self) -> list[Category]: ...
    def get_by_id(self, category_id: int) -> Category: ...
    def get_tree(self) -> list[Category]: ...
    def update(self, category_id: int, data: CategoryUpdate) -> Category: ...
    def delete(self, category_id: int) -> None: ...
```
