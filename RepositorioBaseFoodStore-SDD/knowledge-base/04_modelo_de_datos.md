# Modelo de Datos

## Dominios
El esquema relacional de la base de datos PostgreSQL está estrictamente modelado en **Tercera Forma Normal (3FN)**, implementando a lo largo de todas las entidades de negocio patrones de **Soft Delete** (mediante la columna `eliminado_en` de tipo `TIMESTAMPTZ` o `TIMESTAMP` nullable) y campos transversales de auditoría automáticos (`creado_en` y `actualizado_en`).

Se organiza lógicamente en tres dominios verticales:
1. **Identidad y Acceso**: Gestión de cuentas de usuario, control de acceso basado en roles (RBAC), tokens de refresco opacos para rotación segura y libretas de direcciones de entrega del cliente.
2. **Catálogo de Productos**: Estructuración del inventario, modelado de categorías jerárquicas autoreferenciales, productos con stock atómico directo y composición de ingredientes con banderas de alérgenos.
3. **Ventas, Pagos y Trazabilidad**: Agregado raíz de órdenes de compra implementando el patrón Snapshot inmutable en líneas de pedido y cabeceras, junto con un audit trail con semántica estrictamente append-only y persistencia de transacciones idempotentes de MercadoPago.

## ERD (Entity Relationship Diagram)
```
+-------------------+             +-------------------+             +-------------------+
|      Usuario      |1           N|    UsuarioRol     |N           1|        Rol        |
|-------------------|-------------|-------------------|-------------|-------------------|
| id (PK)           |             | usuario_id (PK/FK)|             | codigo (PK)       |
| email (UQ)        |             | rol_codigo (PK/FK)|             | nombre            |
| password_hash     |             +-------------------+             +-------------------+
| nombre            |
| telefono          |
| eliminado_en      |
+---------+---------+
          |1
          |-----------------------------------------+
          |N                                        |N
+---------+---------+                     +---------+---------+
|   RefreshToken    |                     | DireccionEntrega  |
|-------------------|                     |-------------------|
| token_hash (PK)   |                     | id (PK)           |
| usuario_id (FK)   |                     | linea1            |
| expires_at        |                     | es_principal      |
| revoked_at        |                     | es_principal      |
+-------------------+                     +---------+---------+
                                                    |1
                                                    |
+-------------------+                               |
|     Categoria     |1                              |
|-------------------|--+                            |
| id (PK)           |  | parent_id                  |
| nombre            |<-+ (FK self-ref)              |
+---------+---------+                               |
          |1                                        |
          |N                                        |
+---------+---------+     +-------------------+     |     +-------------------+
| ProductoCategoria |     |     Producto      |     |     |     FormaPago     |
|-------------------|    1|-------------------|     |    1|-------------------|
| producto_id(PK/FK)|-----| id (PK)           |     |     | codigo (PK)       |
| cat_id (PK/FK)    |N    | nombre            |     |     | habilitado        |
+-------------------+     | precio_base       |     |     +---------+---------+
                          | stock_cantidad    |     |               |1
                          | disponible        |     |               |
                          +---------+---------+     |               |
                                    |1              |               |
                                    |N              |               |
+-------------------+     +---------+---------+     |     +---------+---------+
|    Ingrediente    |1   N|ProductoIngrediente|     |     |      Pedido       |
|-------------------|-----|-------------------|     |    N|-------------------|
| id (PK)           |     | producto_id(PK/FK)|     +-----| direccion_id (FK) |
| nombre (UQ)       |     | ingrediente_id    |           | forma_pago (FK)   |
| es_alergeno       |     | es_removible      |           | estado_codigo(FK) |
+-------------------+     +-------------------+           | total (Snapshot)  |
                                                          | dir_snapshot      |
                                                          +---------+---------+
                                                                    |1
                                        +---------------------------+---------------------------+
                                        |1                          |1                          |1
                                        |N                          |N                          |N
                              +---------+---------+       +---------+---------+       +---------+---------+
                              |   DetallePedido   |       |HistorialEstadoPed.|       |       Pago        |
                              |-------------------|       |-------------------|       |-------------------|
                              | id (PK)           |       | id (PK)           |       | id (PK)           |
                              | pedido_id (FK)    |       | pedido_id (FK)    |       | pedido_id (FK)    |
                              | producto_id (FK)  |       | estado_desde (FK) |       | mp_payment_id (UQ)|
                              | nombre_snapshot   |       | estado_hasta (FK) |       | mp_status         |
                              | precio_snapshot   |       | created_at        |       | external_ref (UQ) |
                              | personalizacion   |       | observacion       |       | idempotency_key   |
                              | (INTEGER[])       |       +-------------------+       +-------------------+
                              +-------------------+
```

## Entidades
### Usuario
- **Atributos**: `id` (`BIGSERIAL`/`BIGINT`), `nombre` (`VARCHAR`), `email` (`VARCHAR(254)` con validación estricta), `password_hash` (`CHAR(60)`), `telefono` (`VARCHAR` nullable), `creado_en` (`TIMESTAMPTZ`), `actualizado_en` (`TIMESTAMPTZ`), `eliminado_en` (`TIMESTAMPTZ` nullable).
- **Relaciones**: Muchos a Muchos con `Rol` (vía `UsuarioRol`), Uno a Muchos con `RefreshToken`, Uno a Muchos con `DireccionEntrega`, Uno a Muchos con `Pedido`.
- **Constraints**: `UNIQUE(email)`, PK en `id`.
- **Índices**: Índice B-Tree sobre `email` para optimizar búsquedas en el login.

### Rol y UsuarioRol
- **Rol**: Tabla catálogo estática con PK semántica en `codigo` (`VARCHAR(20)`). Registros: `ADMIN`, `STOCK`, `PEDIDOS`, `CLIENT`.
- **UsuarioRol**: Pivote con PK compuesta `(usuario_id, rol_codigo)` garantizando unicidad de asignación.

### RefreshToken
- **Atributos**: `token_hash` (`CHAR(64)` PK, almacenando hash seguro SHA-256 del token emitido), `usuario_id` (`BIGINT` FK), `expires_at` (`TIMESTAMPTZ`), `revoked_at` (`TIMESTAMPTZ` nullable).

### DireccionEntrega
- **Atributos**: `id` (`BIGSERIAL`), `usuario_id` (`BIGINT` FK), `alias` (`VARCHAR(50)`), `linea1` (`TEXT`), `es_principal` (`BOOLEAN` default false).

### Categoria
- **Atributos**: `id` (`BIGSERIAL`), `nombre` (`VARCHAR(100)`), `parent_id` (`BIGINT` FK autoreferencial nullable apuntando a `Categoria.id`).
- **Constraints**: `ON DELETE SET NULL` en `parent_id` para evitar destrucción en cascada de subcategorías.

### Producto
- **Atributos**: `id` (`BIGSERIAL`), `nombre` (`VARCHAR(150)`), `precio_base` (`DECIMAL(10,2)` o `NUMERIC`), `stock_cantidad` (`INTEGER`), `disponible` (`BOOLEAN` default true), `creado_en`, `actualizado_en`, `eliminado_en`.
- **Constraints**: `CHECK (precio_base >= 0)`, `CHECK (stock_cantidad >= 0)`.

### Ingrediente y ProductoIngrediente
- **Ingrediente**: `id` (`BIGSERIAL`), `nombre` (`VARCHAR(100)` UNIQUE), `es_alergeno` (`BOOLEAN` default false).
- **ProductoIngrediente**: Pivote M2M con columna adicional `es_removible` (`BOOLEAN`) que habilita la personalización en carritos.

### Pedido
- **Atributos**: `id` (`BIGSERIAL`), `usuario_id` (`BIGINT` FK), `estado_codigo` (`VARCHAR(20)` FK hacia `EstadoPedido`), `forma_pago_codigo` (`VARCHAR(20)` FK), `direccion_id` (`BIGINT` FK nullable para permitir retiro en local), `total` (`DECIMAL(10,2)` Snapshot), `costo_envio` (`DECIMAL(10,2)`), `direccion_snapshot` (`TEXT` JSON serializado).

### DetallePedido
- **Atributos**: `id` (`BIGSERIAL`), `pedido_id` (`BIGINT` FK), `producto_id` (`BIGINT` FK), `cantidad` (`INTEGER`), `nombre_snapshot` (`VARCHAR(200)`), `precio_snapshot` (`DECIMAL(10,2)`), `personalizacion` (`INTEGER[]` nativo almacenando IDs de ingredientes excluidos).
- **Constraints**: `CHECK (cantidad >= 1)`.

### HistorialEstadoPedido
- **Atributos**: `id` (`BIGSERIAL`), `pedido_id` (`BIGINT` FK), `estado_desde` (`VARCHAR(20)` FK nullable), `estado_hasta` (`VARCHAR(20)` FK), `usuario_id` (`BIGINT` FK nullable), `created_at` (`TIMESTAMPTZ`), `observacion` (`TEXT`).
- **Patrón**: Append-only estricto en BD.

### Pago
- **Atributos**: `id` (`BIGSERIAL`), `pedido_id` (`BIGINT` FK), `mp_payment_id` (`BIGINT` UNIQUE nullable), `mp_status` (`VARCHAR(30)`), `external_reference` (`VARCHAR(100)` UNIQUE), `idempotency_key` (`VARCHAR(100)` UNIQUE).

## Seed data inicial
El script de seed es idempotente (`INSERT ... ON CONFLICT DO NOTHING`) y precarga:
1. **Roles**: `ADMIN`, `STOCK`, `PEDIDOS`, `CLIENT`.
2. **EstadoPedido**: `PENDIENTE`, `CONFIRMADO`, `EN_PREP`, `EN_CAMINO`, `ENTREGADO` (es_terminal=true), `CANCELADO` (es_terminal=true).
3. **FormaPago**: `MERCADOPAGO`, `EFECTIVO`, `TRANSFERENCIA` (todas habilitadas).
4. **Superusuario**: Cuenta `admin@foodstore.com` con rol `ADMIN` precargado.
