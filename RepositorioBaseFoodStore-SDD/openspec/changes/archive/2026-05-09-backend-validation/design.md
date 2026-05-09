## Context

Actualmente los modelos de dominio están implementados con SQLModel en `core/models.py`. Sin embargo, las rutas de la API no utilizan esquemas Pydantic puros (DTOs) para validar estrictamente las peticiones, lo cual podría llevar a vulnerabilidades de asignación masiva o lógica de negocio inválida en los controladores.

## Goals / Non-Goals

**Goals:**
- Implementar validación y sanitización estricta de datos entrantes en los endpoints del backend.
- Separar las representaciones de los datos entrantes (Pydantic DTOs) de los modelos ORM (SQLModel).

**Non-Goals:**
- Refactorizar las tablas de la base de datos subyacente.
- Cambiar la lógica de negocio de los servicios más allá del pasaje de parámetros.

## Decisions

**Approach 1: Schemas dedicados (DTOs)**
Se decide crear un módulo nuevo en `backend/app/schemas/` que alojará los modelos `Pydantic` de request y response.
- **Alternativa considerada:** Añadir `@field_validator` a los modelos SQLModel directamente.
- **Razón del rechazo:** Mezcla la persistencia de datos (ORM) con el tipado de HTTP requests, lo cual expone campos y causa asimetrías difíciles de manejar (ej. confirmar contraseñas).

## Risks / Trade-offs

- **Risk:** Duplicación leve de definiciones de tipos (ej. nombre y email en el DTO y en el modelo DB).
  - **Mitigation:** Utilizar clases base en Pydantic si resulta práctico, pero primar la claridad del DTO por sobre la evitación de código boilerplate.

## Migration Plan

La actualización se hará in-place sobre los endpoints existentes dado que estamos en fase inicial. No requiere migración de datos.