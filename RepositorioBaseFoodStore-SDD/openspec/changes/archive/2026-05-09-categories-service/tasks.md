# Tasks: categories-service

## Implementation Checklist

- [x] Crear `CategoryRepository` heredando de `BaseRepository` con métodos para subcategorías y raíz.
- [x] Inyectar `CategoryRepository` en `AppUnitOfWork`.
- [x] Crear `backend/categories/schemas.py` para Pydantic DTOs (Create, Update, Read, Jerárquico).
- [x] Crear `backend/categories/service.py` con `CategoriesService`.
- [x] Implementar validación para evitar nombres duplicados.
- [x] Implementar validación para prevenir auto-referencias parent-child.
- [x] Implementar bloqueo de eliminación para categorías con subcategorías.
