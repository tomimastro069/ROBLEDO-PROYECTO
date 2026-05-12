# Actores y Roles

## Actores del sistema
| Actor | Descripción | Cómo interactúa |
| :--- | :--- | :--- |
| **Cliente** | Usuario final de la tienda de comidas. | Se registra, inicia sesión, navega el árbol de categorías y el catálogo, personaliza productos excluyendo ingredientes, añade ítems a su carrito persistente, gestiona sus direcciones de entrega, confirma pedidos y realiza pagos tokenizados con MercadoPago. Solo visualiza y opera sobre sus propios registros. |
| **Administrador (Admin)** | Superusuario con control integral y visibilidad absoluta de todas las entidades. | Administra las cuentas de usuario (crear, editar, desactivar) y asigna roles mediante RBAC. Posee acceso irrestricto al catálogo completo, al panel de métricas y a todos los pedidos (pudiendo cancelar excepcionalmente órdenes ya en preparación). |
| **Gestor de Stock** | Encargado del inventario y la correcta categorización y composición del catálogo. | Consulta y modifica el campo `stock_cantidad` y el toggle `disponible` de los productos. Gestiona la tabla de ingredientes (marcando explícitamente alérgenos) y estructura el árbol jerárquico de categorías. Carece de acceso a pedidos, usuarios y finanzas. |
| **Gestor de Pedidos** | Responsable operativo de la cocina y el despacho de las órdenes. | Visualiza en tiempo real la cola global de pedidos del sistema. Avanza el estado de las órdenes siguiendo estrictamente la máquina de estados finitos (FSM) desde `CONFIRMADO` $\to$ `EN_PREPARACIÓN` $\to$ `EN_CAMINO` $\to$ `ENTREGADO`. Puede cancelar órdenes pendientes o confirmadas. No accede a catálogo ni usuarios. |
| **Sistema** | Conjunto de procesos y demonios automatizados del servidor. | Recibe y verifica webhooks IPN entrantes de MercadoPago, actualiza estados de transacciones, dispara el avance automático de pedidos de `PENDIENTE` $\to$ `CONFIRMADO` (decrementando stock de forma atómica), y revoca/rota tokens de acceso y refresco. |

## RBAC — Matriz de permisos
Los roles en base de datos poseen identificadores fijos y estables cargados en la tabla `Rol` mediante el script de seed obligatorio: `ADMIN` (1), `STOCK` (2), `PEDIDOS` (3) y `CLIENT` (4). Un usuario puede poseer múltiples roles de forma concurrente.

| Rol | Recurso | Permisos (CRUD) |
| :--- | :--- | :--- |
| **ADMIN** | Usuarios y Roles | CRUD completo. Asignación y revocación irrestricta de roles a terceros. |
| **ADMIN** | Catálogo, Stock y Pedidos | CRUD completo. Visibilidad global. Acceso a métricas de negocio. |
| **STOCK** | Productos, Categorías e Ingred. | CRUD completo sobre entidades de catálogo. Modificación de stock y alérgenos. |
| **STOCK** | Pedidos, Usuarios, Finanzas | Sin acceso (HTTP 403 Forbidden). |
| **PEDIDOS** | Pedidos e Historiales | Lectura global de órdenes. Modificación restringida (Avance FSM y Cancelación permitida). |
| **PEDIDOS** | Catálogo y Usuarios | Sin acceso (HTTP 403 Forbidden). |
| **CLIENT** | Pedidos y Direcciones Propias | Creación y Lectura (restringida exclusivamente a registros donde `usuario_id` coincide con el JWT). |
| **CLIENT** | Catálogo Público | Lectura filtrada (solo productos donde `disponible = true` y `eliminado_en IS NULL`). |

## Rutas públicas
Las siguientes rutas de la API REST son accesibles de forma completamente anónima (sin requerir el envío de un token Bearer válido en el header `Authorization`):
- `POST /api/v1/auth/login`: Autenticación y emisión de tokens (protegido perimetralmente por rate limiting de 5 intentos/15 min).
- `POST /api/v1/auth/register`: Registro de nuevas cuentas de cliente.
- `POST /api/v1/auth/refresh`: Renovación opaca de access tokens utilizando un refresh token válido.
- `GET /api/v1/productos`: Catálogo general público (excluye elementos ocultos o lógicamente eliminados).
- `GET /api/v1/productos/{id}`: Detalle de producto e ingredientes.
- `GET /api/v1/productos/{id}/ingredientes`: Listado de componentes y alérgenos.
- `GET /api/v1/categorias`: Árbol completo de categorías jerárquicas precalculado.
- `POST /api/v1/pagos/webhook`: Punto de entrada asíncrono para notificaciones IPN de MercadoPago.
