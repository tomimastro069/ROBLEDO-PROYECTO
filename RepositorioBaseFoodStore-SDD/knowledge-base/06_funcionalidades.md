# Funcionalidades

## Módulos y épicas del sistema
El backend se organiza bajo una filosofía puramente **Feature-First**, alojando todo el código propio de cada dominio dentro de su respectiva subcarpeta en `app/modules/`. De forma complementaria, el frontend divide sus vistas y lógica mediante **Feature-Sliced Design (FSD)** en `src/features/`.

### 1. Módulo Auth (`app/modules/auth/`)
- **Gestión de ciclo de vida de sesión**: Registro de nuevos usuarios, inicio de sesión seguro emitiendo pares de tokens JWT asimétricos en tiempo de vida (Access y Refresh).
- **Protección perimetral**: Integración nativa de limitadores de tasa (SlowAPI) para mitigar ataques de fuerza bruta.
- **Cierre de sesión seguro**: Revocación explícita marcando con un timestamp la columna `revoked_at` en la tabla `RefreshToken` para deshabilitar su uso futuro.

### 2. Módulo Usuarios (`app/modules/usuarios/`)
- **Administración de cuentas**: Operaciones CRUD completas reservadas para administradores, aplicando el patrón de eliminación lógica (Soft Delete) para preservar la integridad referencial de los historiales de pedidos de clientes inactivos.
- **Asignación de roles**: Gestión ágil de la tabla pivote `UsuarioRol` para conferir permisos de forma granular (RBAC).

### 3. Módulo Direcciones (`app/modules/direcciones/`)
- **Libreta de entregas**: Permite a cada cliente mantener múltiples ubicaciones de envío con alias semánticos ("Casa", "Oficina").
- **Dirección principal**: Endpoint especializado (`PATCH /principal`) que asegura de forma transaccional que un usuario posea exactamente una única dirección marcada con el flag `es_principal = true`.

### 4. Módulo Categorías (`app/modules/categorias/`)
- **Estructura arbórea infinita**: Soporte para anidamiento recursivo arbitrario consultado eficientemente mediante Common Table Expressions (CTE) en PostgreSQL.
- **Protección de integridad**: Eliminación lógica suave con reasignación en cascada (`ON DELETE SET NULL`) para evitar la orfandad de productos activos.

### 5. Módulo Productos (`app/modules/productos/`)
- **Catálogo de alta fidelidad**: Listado paginado con soporte de filtrado múltiple (categoría, estado, búsqueda por texto).
- **Gestión de stock en tiempo real**: Actualización atómica de las cantidades disponibles y control manual del conmutador de visibilidad (`disponible`).
- **Trazabilidad de ingredientes y alérgenos**: Asociación de componentes con banderas de remoción (`es_removible`) para personalización y alertas visuales automáticas ante ingredientes marcados como `es_alergeno`.

### 6. Módulo Pedidos (`app/modules/pedidos/`)
- **Máquina de estados finitos (FSM)**: Transición centralizada y validada a lo largo del ciclo de vida del pedido.
- **Preservación inmutable (Snapshot)**: Congelamiento estático de precios y datos del catálogo al momento de la compra para aislar la contabilidad histórica.
- **Auditoría continua**: Registro append-only en `HistorialEstadoPedido` con trazabilidad completa de cada evento, actor y motivo.

### 7. Módulo Pagos (`app/modules/pagos/`)
- **Pasarela MercadoPago Checkout API**: Integración completa sin redirección externa para el procesamiento de cobros con tarjeta, efectivo o transferencias.
- **Gestión de Idempotencia**: Generación y resguardo de UUIDs únicos (`idempotency_key`) para mitigar transacciones duplicadas por intermitencias de red.
- **Recepción asíncrona (Webhooks IPN)**: Escucha pasiva de eventos de MercadoPago para actualizar automáticamente el estado financiero y despachar órdenes.

### 8. Módulo Admin (`app/modules/admin/`)
- **Tableros de inteligencia de negocio**: Paneles de control con métricas clave (KPIs) e integración con `recharts` para la graficación temporal de ingresos y volúmenes de pedidos.
- **Consola de despacho**: Interfaz de alta densidad para la gestión eficiente de las colas de cocina y stock por parte del personal interno.
