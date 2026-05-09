# Proposal: Validación de Backend

## Intent

Implementar validación y sanitización estricta de inputs para la API del backend mediante el uso de esquemas dedicados (DTOs), protegiendo la base de datos de asignaciones masivas y garantizando que las reglas de negocio en los datos de entrada se cumplan antes de llegar a los controladores.

## Scope

### In Scope
- Creación del directorio `backend/app/schemas/`.
- Creación de DTOs con Pydantic para creación y actualización de modelos principales (User, Product, Category, etc.).
- Integración de los esquemas en los endpoints de la API.
- Reflejar la tarea como completada en `RepositorioBaseFoodStore-SDD/docs/map/map.md`.

### Out of Scope
- Modificación de los modelos de base de datos (`SQLModel`) en `core/models.py`.
- Creación de nuevos endpoints.
- Validaciones cruzadas complejas de base de datos que pertenecen a servicios de dominio.

## Approach

**Approach 1 (Schemas dedicados)**: Se separará la validación de peticiones HTTP de los modelos de base de datos. Se crearán modelos puros de Pydantic (ej. `UserCreate`, `ProductCreate`) en un nuevo módulo `schemas` para manejar las validaciones asimétricas. El manejador global de excepciones RFC 7807 ya existente se encargará de reportar los errores 422 generados.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `backend/app/schemas/` | New | Módulos Pydantic para DTOs |
| `backend/app/api/` | Modified | Actualización de tipos de entrada en endpoints |
| `RepositorioBaseFoodStore-SDD/docs/map/map.md` | Modified | Marcar tarea 9 como completada |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Duplicación de campos entre BD y API | Med | Aceptar leve duplicación en favor de una separación clara de responsabilidades y seguridad. |
| Errores de mapeo | Low | Asegurar tipado correcto al pasar de DTO a modelo ORM antes de invocar los repositorios. |

## Rollback Plan

Revertir los commits relacionados con la creación de los DTOs y restaurar las firmas originales de las rutas en `backend/app/api/`.

## Dependencies

- Manejo de excepciones RFC 7807 (`backend-error-handling` ya completado).

## Success Criteria

- [ ] Pydantic intercepta inputs inválidos y retorna un 422 con formato RFC 7807 de forma consistente.
- [ ] La capa de base de datos no es responsable de validar formatos específicos de petición (ej. contraseñas seguras).
- [ ] La tarea 9 está tildada como `[X]` en el mapa de progreso.
