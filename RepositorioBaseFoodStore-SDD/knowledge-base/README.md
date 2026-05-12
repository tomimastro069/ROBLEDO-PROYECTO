# Base de Conocimiento Canónica — Food Store v5.0

Esta base de conocimiento (*Knowledge Base*) constituye la única fuente de verdad técnica y funcional para el desarrollo, evolución y auditoría del sistema **Food Store** bajo el paradigma de **Spec-Driven Development (SDD)**.

Todos los artefactos contenidos en este directorio han sido sintetizados e indexados de forma automatizada y estructurada a partir de la documentación original del proyecto (`docs/Descripcion.txt`, `docs/Historias_de_usuario.txt`, `docs/Integrador.txt`), reflejando de manera fiel la arquitectura de capas, el diseño relacional y las reglas de negocio fundacionales.

## Estructura de Archivos e Índice de Contenidos

| Archivo | Temas Cubiertos |
| :--- | :--- |
| `01_vision_y_objetivos.md` | Propósito integral del e-commerce, desglose de objetivos por actor, alcance detallado de la versión 5.0, exclusiones y métricas de éxito del negocio. |
| `02_descripcion_general.md` | Matriz del stack tecnológico full-stack (React/Vite/FastAPI), diagramas de arquitectura global, flujo unidireccional de dependencias e integraciones externas. |
| `03_actores_y_roles.md` | Definición de los cinco actores del sistema, matriz estricta de permisos RBAC para los 4 roles predefinidos y listado de rutas públicas de la API REST. |
| `04_modelo_de_datos.md` | Estructuración en 3 dominios, diagrama ERD en arte ASCII, modelado en 3FN con soporte de soft-delete, detalles de columnas/constraints y carga de datos semilla. |
| `05_reglas_de_negocio.md` | Las cinco reglas inmutables del dominio central de pedidos (FSM, append-only, snapshots) y las cinco normas críticas de seguridad y hashing de contraseñas. |
| `06_funcionalidades.md` | Desglose y organización de responsabilidades bajo el patrón Feature-First para los ocho módulos del backend y Feature-Sliced Design del frontend. |
| `07_flujos_principales.md` | Diagramas de secuencia paso a paso ilustrando la transaccionalidad atómica del Unit of Work al crear pedidos y el ciclo de vida de tokenización de pagos con MercadoPago. |
| `08_arquitectura_propuesta.md` | Evaluación comparativa de tres opciones de persistencia, justificación del patrón Unit of Work + Repositorios Genéricos y sus ventajas de testabilidad. |
| `09_decisiones_y_supuestos.md` | Registros de Decisiones de Arquitectura (ADRs) documentando el uso de CTE recursivos para categorías, Arrays de PostgreSQL para exclusiones y aislamiento de estado en React. |
| `10_preguntas_abiertas.md` | Repositorio de dudas operativas, umbrales transaccionales y dependencias de producto pendientes de definición en futuras iteraciones. |
| `11_pagos_mercadopago.md` | Dominio extra profundizando en el cumplimiento PCI DSS SAQ-A, claves de idempotencia, mapeo de webhooks IPN y listado de tarjetas Sandbox oficiales. |
| `12_gestion_de_estado_zustand.md` | Dominio extra documentando la estructura interna, responsabilidades, persistencia selectiva y buenas prácticas de consumo de los 4 stores globales de Zustand. |

## Mantenimiento y Evolución
Cualquier propuesta de cambio, refactorización o nueva funcionalidad (`Change`) gestionada a través de `openspec` debe obligatoriamente consultar y respetar los lineamientos, restricciones y patrones descritos en esta base de conocimiento antes de la fase de implementación.
