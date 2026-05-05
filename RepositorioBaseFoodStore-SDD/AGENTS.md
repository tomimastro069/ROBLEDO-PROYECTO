# AGENTS.md

## Propósito

Este archivo detalla las capacidades de los agentes inteligentes disponibles en el proyecto. Los agentes automatizan tareas frecuentes y aceleran el flujo de trabajo basado en el modelo de Desarrollo Guiado por Especificaciones (SDD por sus siglas en inglés). Las herramientas y habilidades aquí descritas están diseñadas para apoyar tanto el backend como el frontend del proyecto, así como el dominio específico de la plataforma.

---

## Habilidades Disponibles

### Habilidades de OpenSpec (Flujo de trabajo SDD)

Estas habilidades están instaladas en `.agent/skills/` y `.agents/skills/`, y soportan el proceso completo de desarrollo guiado por especificaciones:

| **Habilidad**              | **Comando/Disparador**         | **Propósito**                                                                 |
|-----------------------------|-------------------------------|-------------------------------------------------------------------------------|
| **openspec-explore**        | `/openspec:explore <tema>`    | Explorar ideas, investigar problemas y clarificar requerimientos.            |
| **openspec-propose**        | `/openspec:propose <desc>`    | Generar una propuesta completa incluyendo intención, alcance y enfoque.       |
| **openspec-apply-change**   | `/openspec:apply`             | Implementar tareas definidas siguiendo las especificaciones propuestas.       |
| **openspec-archive-change** | `/openspec:archive`           | Finalizar y archivar un cambio tras su implementación.                        |
| **find-skills**             | "how do I...", "find a skill..." | Descubrir e instalar habilidades adicionales según necesidades del proyecto. |

### Habilidades del Sistema (Globales)

Estas habilidades están disponibles globalmente desde `~/.config/opencode/skills/` y proporcionan soporte adicional:

| **Habilidad**                    | **Comando/Disparador**            | **Propósito**                                                                  |
|-----------------------------------|-----------------------------------|--------------------------------------------------------------------------------|
| **sdd-init**                      | `sdd init`                       | Inicializar el contexto SDD, detectando el stack y las convenciones.          |
| **python-fastapi-development**    | Automático                       | Mejores prácticas para proyectos backend con FastAPI.                         |
| **natural-language-postgres**     | Automático                       | Habilitar consultas PostgreSQL utilizando lenguaje natural.                   |
| **betterauth-fastapi-jwt-bridge** | Automático                       | Gestión robusta de JWT y autorización avanzada en FastAPI.                   |
| **sdd-onboard**                   | Despliegue del orquestador       | Guiar el ciclo SDD completo usando el entorno real.                           |
| **sdd-explore**                   | Despliegue del orquestador       | Explorar ideas antes de comprometer cambios o especificaciones.               |
| **sdd-propose**                   | Despliegue del orquestador       | Crear propuestas de cambios con intención, alcance y diseño.                  |

---

## Configuración del Proyecto

### Persistencia
- **Modo activo**: `openspec` (basado en archivos, amigable con Git).
- **Ubicación**: Carpeta `openspec/` (contiene `config.yaml`, `specs/`, `changes/`, `archive/`).
- **Disponibilidad adicional**: Engram (memoria persistente entre sesiones) para conservar contexto.

### Strict TDD Mode
- **Estado**: ❌ Desactivado.
- **Razón**: Las herramientas de testing backend/frontend aún no están configuradas.
- **Habilitación**: Configurar con pytest (backend) y vitest (frontend), luego ejecutar `/sdd-init` otra vez.

### Stack Tecnológico

**Backend**:
- Framework: FastAPI (Python 3.11+).
- Base de datos: PostgreSQL 15+ con Alembic para migraciones.
- ORM: SQLModel (SQLAlchemy + Pydantic).

**Frontend**:
- Framework: React + TypeScript.
- Librerías: Zustand + TanStack Query.
- Bundle: Vite.

### Actores Clave
- **Cliente**: Usuario final del sistema.
- **Administrador**: Control global del sistema.
- **Gestor de Stock**: Inventarios y actualizaciones operativas.
- **Sistema (Integrador)**: Automatización/MercadoPago.

---

## Próximos Pasos

- Crear e instalar dependencias en `requirements.txt` y `package.json`.
- Verificar el flujo completo con pruebas unitarias activadas.
