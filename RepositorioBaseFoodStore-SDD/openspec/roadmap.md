# Roadmap de Implementación

Mapa completo de changes para desarrollar **Food Store v5.0** de inicio a fin.
Generado a partir de `knowledge-base/` el 2026-05-12.

---

## Orden de ejecución

| # | Change | Funcionalidad | US | Depende de | Razón de la dependencia |
|---|--------|---------------|-----|------------|--------------------------|
| 1 | `us-000-setup` | Infraestructura base | US-000 | — | Punto de partida |
| 2 | `us-001-auth` | JWT + RBAC + refresh | US-001 a US-005 | `us-000-setup` | Requiere backend operativo y estructura de base de datos |
| 3 | `us-002-categorias` | Catálogo jerárquico | US-010 a US-014 | `us-001-auth` | Endpoints CRUD y de gestión requieren rol ADMIN/STOCK |
| 4 | `us-003-productos` | CRUD + stock + ingredientes | US-015 a US-024 | `us-002-categorias` | `Producto.categoria_id` referencia el árbol de categorías |
| 5 | `us-004-carrito` | Estado client-side con Zustand | US-030 a US-034 | `us-003-productos` | Necesita catálogo de productos disponible y consumible |
| 6 | `us-005-pedidos` | UoW + FSM + audit trail | US-040 a US-052 | `us-004-carrito` | Convierte el carrito cliente en un pedido persistido con snapshots |
| 7 | `us-006-pagos` | MercadoPago Checkout + webhook IPN | US-055 a US-062 | `us-005-pedidos` | La orden de cobro se asocia unívocamente a la cabecera de un pedido |
| 8 | `us-007-admin` | Panel admin + métricas | US-065 a US-072 | `us-006-pagos` | Gráficos y reportes consumen historiales de pedidos y estados de pago |
| 9 | `us-008-direcciones` | Direcciones de entrega del cliente | US-075 a US-076 | `us-001-auth` | Independiente de pedidos pero requiere la existencia de cuentas de usuario |
| 10 | `admin-dashboard-crud` | Panel admin CRUD (Categorías, Ingredientes, Productos, Pedidos) | — | `us-002-categorias`, `us-003-productos` | Consume endpoints CRUD ya implementados del backend |

---

## Detalle por change

### 1. `us-000-setup`

**Funcionalidad**: Configuración de la estructura de directorios modular, gestión de dependencias backend (FastAPI, SQLModel, Alembic, slowapi) y frontend (React, Vite, Zustand, TanStack Query), archivo `.env` inicial, conexión a PostgreSQL y generación de migración inicial vacía.

**US implementadas**: US-000.

**Depende de**: ninguno (punto de partida).

**Justificación**: Todos los desarrollos posteriores asumen como garantizada la existencia de la base de datos física, la estructura de carpetas bajo Feature-First/FSD y las variables de entorno inyectadas.

**Riesgos / preguntas abiertas**: La correcta inicialización de la base de datos es bloqueante para cualquier prueba local o de integración en los sprints venideros.

---

### 2. `us-001-auth`

**Funcionalidad**: Registro de clientes, inicio de sesión seguro emitiendo JWT con arquitectura de doble token (Access en Zustand y Refresh con expiración de 7 días), hashing con `passlib` (`bcrypt` con factor de costo $\ge 12$), tabla `RefreshToken` para invalidación y revocación explícita, y protección perimetral de fuerza bruta mediante `slowapi`.

**US implementadas**: US-001 a US-005.

**Depende de**: `us-000-setup`.

**Justificación**: Establece la identidad (`Usuario`) y los 4 roles estables del sistema (`ADMIN`, `STOCK`, `PEDIDOS`, `CLIENT`). Sin esta capa fundacional, es imposible proteger los endpoints de catálogo de gestión o validar la propiedad sobre carritos y pedidos.

**Riesgos / preguntas abiertas**: Ver pregunta abierta 4 en `10_preguntas_abiertas.md` sobre el procedimiento operativo estándar para invalidar globalmente sesiones ante un compromiso de la `SECRET_KEY`.

---

### 3. `us-002-categorias`

**Funcionalidad**: Estructuración del inventario mediante un árbol jerárquico recursivo de profundidad ilimitada, resuelto en consultas de base de datos a través de Common Table Expressions (CTE recursivas en PostgreSQL) y eliminación lógica suave con retención en cascada (`ON DELETE SET NULL`).

**US implementadas**: US-010 a US-014.

**Depende de**: `us-001-auth`.

**Justificación**: Los endpoints de creación, modificación y borrado de categorías exigen permisos restringidos correspondientes a los roles de administración o inventario.

**Riesgos / preguntas abiertas**: Ninguno crítico.

---

### 4. `us-003-productos`

**Funcionalidad**: Catálogo general paginado de alta fidelidad, gestión de stock atómico directo (`stock_cantidad`), control manual del toggle de visibilidad (`disponible`), y asociación de componentes mediante la tabla pivote `ProductoIngrediente` con banderas de remoción (`es_removible`) y de alérgenos (`es_alergeno`).

**US implementadas**: US-015 a US-024.

**Depende de**: `us-002-categorias`.

**Justificación**: La tabla `Producto` posee una clave foránea que referencia la categoría a la que pertenece. Por ende, la entidad referenciada debe existir y estar estabilizada en el esquema antes de implementar el producto.

**Riesgos / preguntas abiertas**: Ninguno crítico.

---

### 5. `us-004-carrito`

**Funcionalidad**: Almacenamiento local puramente en el cliente de los ítems seleccionados para compra, gestionado a través de Zustand (`cartStore.ts`) con selectores atómicos para cómputos de subtotales y persistencia íntegra en `localStorage`.

**US implementadas**: US-030 a US-034.

**Depende de**: `us-003-productos`.

**Justificación**: El carrito requiere consumir la información estable del catálogo (IDs, nombres e imágenes de producto) para permitir la adición de ítems y la selección de ingredientes a excluir.

**Riesgos / preguntas abiertas**: Ver pregunta abierta 2 en `10_preguntas_abiertas.md` respecto a la ausencia de un límite superior estricto sobre la cantidad máxima de un mismo ítem para evitar bloqueos de stock abusivos.

---

### 6. `us-005-pedidos`

**Funcionalidad**: Dominio transaccional central orquestado mediante el patrón **Unit of Work** para garantizar atomicidad ACID. Implementa una máquina de estados finitos (FSM) de 6 estados con validaciones estrictas de avance, audit trail append-only en `HistorialEstadoPedido` (con estado inicial nulo en base a **RN-02**) y la copia estática inmutable de precios y nombres en las líneas bajo el patrón Snapshot (**RN-04**).

**US implementadas**: US-040 a US-052.

**Depende de**: `us-004-carrito`.

**Justificación**: Convierte el estado efímero del cliente (los ítems del carrito) en un agregado raíz persistente y auditable en el backend.

**Riesgos / preguntas abiertas**: Es el change de mayor complejidad transaccional. Requiere que los repositorios genéricos y el gestor de contexto del UoW operen sin fisuras para evitar bloqueos mutuos o lecturas sucias en concurrencia.

---

### 7. `us-006-pagos`

**Funcionalidad**: Integración de la pasarela MercadoPago Checkout API (Orders) garantizando cumplimiento PCI DSS SAQ-A mediante tokenización de tarjetas con iframes JS en el navegador. Incorpora protección absoluta contra cobros duplicados mediante claves de idempotencia UUID generadas en backend y un punto de escucha asíncrono para notificaciones Webhook IPN que avanza automáticamente el pedido a `CONFIRMADO`.

**US implementadas**: US-055 a US-062.

**Depende de**: `us-005-pedidos`.

**Justificación**: La orden de pago externa se vincula unívocamente al ID o UUID de un pedido ya insertado en la base de datos.

**Riesgos / preguntas abiertas**: Ver pregunta abierta 1 en `10_preguntas_abiertas.md` sobre los tiempos de espera y políticas de reintento exponencial de MercadoPago ante caídas del servidor de Food Store durante la recepción de un IPN.

---

### 8. `us-007-admin`

**Funcionalidad**: Interfaz de control y tableros de inteligencia de negocio (Dashboard) integrando la librería `recharts` para la graficación temporal de ingresos y cargas operativas, junto con la consola interna de seguimiento y despacho de cocina.

**US implementadas**: US-065 a US-072.

**Depende de**: `us-006-pagos`.

**Justificación**: Un tablero de métricas de negocio carece de utilidad sin la existencia previa de los flujos de pedidos, estados de entrega e historiales financieros de pago que proveen la materia prima de graficación.

**Riesgos / preguntas abiertas**: Ninguno crítico.

---

### 9. `us-008-direcciones`

**Funcionalidad**: Módulo completo para la libreta de direcciones de entrega del cliente, soportando múltiples alias semánticos y garantizando de forma transaccional (`PATCH /principal`) que exista exactamente una única dirección principal predeterminada por cuenta.

**US implementadas**: US-075 a US-076.

**Depende de**: `us-001-auth`.

**Justificación**: Es un módulo altamente independiente del flujo de pedidos directo, pero requiere obligatoriamente la existencia previa de la tabla `Usuario` para establecer la clave foránea de pertenencia.

**Riesgos / preguntas abiertas**: Ver pregunta abierta 3 en `10_preguntas_abiertas.md` sobre la posible integración futura con servicios de geocodificación para calcular tarifas de envío dinámicas.

---

### 10. `admin-dashboard-crud` ✅

**Funcionalidad**: Panel de administración dedicado bajo la ruta `/admin` con sidebar de navegación por rol. Incluye páginas CRUD completas para Categorías, Ingredientes y Productos, junto con el panel de gestión de Pedidos ya existente. Implementa una capa de hooks reutilizables (`useFormModal`, `useConfirmDialog`, `usePagination`) y componentes base (`HelpButton`, `PageContainer`) siguiendo la skill `dashboard-crud-page`. Además agrega el campo `phone` al registro de usuario en frontend y backend.

**Depende de**: `us-002-categorias`, `us-003-productos` (endpoints del backend operativos).

**Justificación**: El panel consume directamente las APIs ya disponibles del backend. No requiere cambios de backend adicionales más allá del campo `phone` en el registro.

**Nota**: Implementado fuera de la metodología SDD estricta, documentado y archivado retroactivamente.

---

## Notas finales

- Este roadmap representa la **secuencia recomendada** para un desarrollo libre de bloqueos. Si el equipo requiere paralelizar trabajo, los changes con dependencias disjuntas pueden implementarse en paralelo (por ejemplo, iniciar `us-008-direcciones` de forma concurrente a `us-003-productos` o `us-005-pedidos`).
- Cada change ha sido diseñado para ser **atómico y mergeable de forma independiente**. Si durante la ejecución de una tarea se detecta una divergencia o una carga superior a la prevista, el change debe partirse y este roadmap debe actualizarse.
- Las dudas registradas en `10_preguntas_abiertas.md` actúan como alertas de riesgo y deben ser clarificadas antes de iniciar la fase de propuesta (`/opsx:propose`) del change afectado.
