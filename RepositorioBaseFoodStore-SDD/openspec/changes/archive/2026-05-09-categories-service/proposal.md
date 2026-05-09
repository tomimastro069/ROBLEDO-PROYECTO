# Proposal: categories-service

## Problem Statement

El backend cuenta con la entidad de dominio `Category` y la base de datos ya está inicializada, pero carece de la lógica de negocio necesaria para gestionar las categorías (creación, lectura, actualización, eliminación). Es fundamental para el e-commerce poder organizar los productos en una estructura jerárquica de categorías y subcategorías.

## Proposed Solution

Implementar un servicio de dominio (`CategoriesService`) y su repositorio asociado (`CategoryRepository`) para encapsular las reglas de negocio de las categorías:
- Repositorio concreto con queries específicas (por nombre, subcategorías, categorías raíz).
- Servicio que valide reglas de negocio antes de persistir (ej. unicidad de nombres, protección de jerarquía, y bloqueo de eliminación si existen hijos).
- Schemas Pydantic para validar entradas y salidas (DTOs).

## Scope

- **In**: CategoryRepository, CategoriesService, Schemas Pydantic.
- **Out**: Endpoints HTTP/Router (esto será cubierto en el change #14 `categories-api`).

## Dependencies

- `backend-uow-and-repositories` [X] — Provee la arquitectura base de UoW y el `BaseRepository`.
