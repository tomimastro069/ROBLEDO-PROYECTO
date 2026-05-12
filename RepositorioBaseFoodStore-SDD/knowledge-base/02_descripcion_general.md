# Descripción General

## Stack tecnológico
| Capa | Tecnologías | Versión mínima | Rol en el sistema |
| :--- | :--- | :--- | :--- |
| **Frontend** | React + TypeScript | 18.x + 5.x | Renderizado de UI, tipado estricto de extremo a extremo, enrutamiento y vistas. |
| **Frontend** | Vite | 5.x | Bundler ultrarrápido basado en ES modules nativos en dev y Rollup en producción. |
| **Frontend** | Tailwind CSS | 3.x | Framework utility-first para el sistema de diseño y estilizado responsivo. |
| **Frontend** | TanStack Query | 5.x | Gestión del estado del servidor (fetching, caching, sincronización y revalidación). |
| **Frontend** | TanStack Form | 0.x | Gestión de estado y validación declarativa de formularios tipados. |
| **Frontend** | Zustand | 4.x | Gestión del estado global del cliente (carrito, sesión, flujo de pago, UI). |
| **Frontend** | Axios | 1.x | Cliente HTTP con interceptores para inyección y renovación transparente de JWT. |
| **Frontend** | recharts | 2.x | Renderizado declarativo de gráficos y métricas en el panel de administración. |
| **Frontend** | @mercadopago/sdk-react | Última | Tokenización segura de tarjetas en el navegador cumpliendo con PCI DSS SAQ-A. |
| **Backend** | FastAPI | 0.111+ | Framework asíncrono de alto rendimiento con autogeneración de OpenAPI. |
| **Backend** | SQLModel | 0.0.19+ | Definición unificada de modelos ORM y esquemas de validación Pydantic. |
| **Backend** | PostgreSQL | 15+ | Motor de base de datos relacional robusto con soporte para CTE y arrays. |
| **Backend** | Alembic | 1.13+ | Herramienta de control de versiones y migraciones incrementales DDL. |
| **Backend** | Passlib (bcrypt) | Última | Hashing seguro de contraseñas con factor de costo $\ge 12$ y salting automático. |
| **Backend** | mercadopago | 2.3.0+ | SDK oficial de Python para integración de la Checkout API y webhooks. |
| **Backend** | slowapi | 0.1.9+ | Rate limiting por IP basado en sliding window protegiendo endpoints críticos. |

## Arquitectura general
El sistema Food Store implementa una arquitectura modular altamente desacoplada, dividida verticalmente por dominios de negocio (Feature-First en el backend y Feature-Sliced Design en el frontend).

```
+-----------------------------------------------------------------------------------+
|                                 FRONTEND (React)                                  |
|                                                                                   |
|  +--------------------+  +--------------------+  +-----------------------------+  |
|  |   Zustand Stores   |  |   TanStack Query   |  |    MercadoPago JS SDK       |  |
|  |  (Client State)    |  |  (Server State)    |  | (Tokenización PCI SAQ-A)    |  |
|  +---------+----------+  +---------+----------+  +--------------+--------------+  |
+------------|-----------------------|----------------------------|-----------------+
             |                       |                            |
      (Acciones / UI)         (Peticiones HTTP)           (Envío directo seguro)
             |                       v                            v
             |             +--------------------+       +--------------------+
             |             |    Axios Client    |       |   MercadoPago API  |
             |             |  (con JWT Interc.) |       |  (Servidores MP)   |
             |             +---------+----------+       +---------+----------+
             |                       |                            |
             +-----------------------+                            | (Webhooks IPN)
                                     |                            |
                                     v                            v
+------------------------------------|----------------------------|-----------------+
|                                 BACKEND (FastAPI)               |                 |
|                                                                 |                 |
|  +---------------------------------+----------------------------+--------------+  |
|  | Layer 1: Router (Validación Pydantic, delegación pura, sin lógica)          |  |
|  +---------------------------------+-------------------------------------------+  |
|                                    v                                              |
|  +---------------------------------+-------------------------------------------+  |
|  | Layer 2: Service (Lógica de negocio, máquina de estados FSM, orquestación)  |  |
|  +---------------------------------+-------------------------------------------+  |
|                                    v                                              |
|  +---------------------------------+-------------------------------------------+  |
|  | Layer 3: Unit of Work (Gestión de transacción atómica, commit/rollback)     |  |
|  +---------------------------------+-------------------------------------------+  |
|                                    v                                              |
|  +---------------------------------+-------------------------------------------+  |
|  | Layer 4: Repository (Hereda de BaseRepository[T], consultas CRUD y CTE)     |  |
|  +---------------------------------+-------------------------------------------+  |
|                                    v                                              |
|  +---------------------------------+-------------------------------------------+  |
|  | Layer 5: Model (Tablas SQLModel mapeadas directamente a PostgreSQL)         |  |
|  +---------------------------------+-------------------------------------------+  |
+------------------------------------|----------------------------------------------+
                                     v
                       +-------------+-------------+
                       |    PostgreSQL Database    |
                       +---------------------------+
```

**Justificación de decisiones de alto nivel:**
1. **Flujo de dependencias estrictamente unidireccional**: En el backend, las capas superiores dependen de las inferiores (`Router` $\to$ `Service` $\to$ `UoW` $\to$ `Repository` $\to$ `Model`), garantizando un aislamiento total de la lógica de negocio y permitiendo pruebas unitarias con mocks del UoW sin tocar la base de datos.
2. **Separación radical del estado en el cliente**: Utilizar Zustand para datos puramente del cliente (carrito persistido, tokens de sesión) y TanStack Query para datos con fuente de verdad en el servidor evita duplicaciones y problemas de sincronización de estado.
3. **Seguridad en procesamiento de pagos**: La tokenización de tarjetas en el navegador delega la responsabilidad del cumplimiento estricto de datos PCI a MercadoPago, minimizando la superficie de ataque en el backend.

## Integraciones externas
| Servicio | Propósito | Tipo (REST / Webhook / SDK) |
| :--- | :--- | :--- |
| **MercadoPago Checkout API** | Creación de órdenes de pago (Orders) y preferencias de cobro seguras. | REST API consumida a través del SDK oficial de Python. |
| **MercadoPago.js / SDK React** | Captura y tokenización segura de datos de tarjetas de crédito/débito en el navegador. | SDK de JavaScript en el cliente. |
| **MercadoPago Webhooks (IPN)** | Recepción asíncrona de cambios de estado en transacciones de pago. | Webhook (POST entrante firmado o validado por API). |

## API REST
Todos los endpoints utilizan el prefijo `/api/v1` y estructuran sus respuestas de error de acuerdo con el estándar **RFC 7807** (Problem Details).
- **Auth**: `/api/v1/auth/login`, `/api/v1/auth/register`, `/api/v1/auth/refresh`, `/api/v1/auth/logout`, `/api/v1/auth/me`.
- **Productos**: `/api/v1/productos` (GET público paginado, POST/PUT/DELETE restringidos), `/api/v1/productos/{id}/ingredientes`.
- **Categorías**: `/api/v1/categorias` (GET público en árbol jerárquico CTE, POST/PUT/DELETE de gestión).
- **Pedidos**: `/api/v1/pedidos` (POST atómico con snapshots, GET filtrado por rol), `/api/v1/pedidos/{id}/estado` (Avance FSM), `/api/v1/pedidos/{id}/historial`.
- **Pagos**: `/api/v1/pagos/crear` (inicia cobro con token), `/api/v1/pagos/webhook` (recepción IPN).
