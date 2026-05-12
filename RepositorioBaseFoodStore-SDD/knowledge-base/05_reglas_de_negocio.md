# Reglas de Negocio

## Reglas del dominio central (Pedidos)
- **RN-01 (Inmutabilidad Terminal)**: Un pedido cuyo estado actual posea el flag `es_terminal = true` en el catálogo `EstadoPedido` (es decir, `ENTREGADO` o `CANCELADO`) se vuelve estrictamente inmutable. La capa de servicio debe rechazar con una excepción de negocio cualquier intento posterior de transición saliente.
- **RN-02 (Transición Raíz)**: El primer registro insertado en la tabla `HistorialEstadoPedido` para un nuevo pedido debe poseer un valor `estado_desde = NULL`, marcando el nacimiento de la entidad en el estado inicial `PENDIENTE`.
- **RN-03 (Audit Trail Append-Only)**: La tabla `HistorialEstadoPedido` es puramente **append-only**. Ningún servicio, controlador o script tiene permitido emitir sentencias `UPDATE` o `DELETE` sobre este historial. Toda la evolución temporal se reconstruye ordenando por `created_at ASC`.
- **RN-04 (Patrón Snapshot en Líneas)**: Para aislar los pedidos históricos de los cambios futuros en el catálogo, al momento de confirmarse un pedido, los campos `precio_base` y `nombre` del producto se copian estáticamente en `precio_snapshot` y `nombre_snapshot` de la tabla `DetallePedido`, utilizándose de forma inmutable para todos los cálculos financieros.
- **RN-05 (Motivo de Cancelación Obligatorio)**: Si se solicita una transición de estado hacia `CANCELADO`, el cliente o administrador está obligado a proveer una cadena de texto no vacía en el campo `motivo`. Caso contrario, la operación se aborta.

## Reglas de seguridad y acceso (Auth)
- **RN-AU01 (Hashing Obligatorio)**: Es un fallo crítico de seguridad almacenar contraseñas en texto plano. Se debe aplicar el algoritmo `bcrypt` a través de la librería `passlib` garantizando un factor de costo mínimo configurado en 12.
- **RN-AU02 (Unicidad de Identidad)**: No pueden coexistir dos usuarios activos o inactivos con la misma dirección de correo electrónico. La validación se realiza a nivel base de datos (`UNIQUE`) y en capa de servicio con validación de formato `EmailStr`.
- **RN-AU03 (Rotación de Refresh Tokens)**: Un token de refresco tiene una validez máxima de 7 días. Tras ser utilizado en `/auth/refresh` o al ejecutar `/auth/logout`, debe marcarse inmediatamente con un timestamp en `revoked_at` para impedir ataques de repetición.
- **RN-AU04 (Aislamiento de Estado Cliente)**: El frontend almacena el `access_token` puramente en el estado persistido de Zustand (`authStore`), prohibiendo el acceso o manipulación manual directa desde componentes fuera de los selectores o el interceptor de Axios.
- **RN-AU05 (Rate Limiting Perimetral)**: El endpoint de inicio de sesión (`POST /api/v1/auth/login`) debe bloquear de forma automática peticiones de una misma dirección IP que superen los 5 intentos fallidos en una ventana móvil de 15 minutos, retornando HTTP 429 Too Many Requests con cabecera `Retry-After`.

## Excepciones
- **Excepción de stock agotado en concurrencia**: Si dos clientes intentan comprar simultáneamente la última unidad disponible de un producto, la transacción de base de datos orquestada por la capa de `Unit of Work` aislará las lecturas/escrituras. El segundo intento detectará `stock_cantidad < cantidad_solicitada` y el UoW ejecutará un `ROLLBACK` completo y limpio, retornando HTTP 409 Conflict o 422 Unprocessable Entity sin dejar registros huérfanos.
- **Excepción de pago rechazado**: Si la pasarela de MercadoPago retorna un estado `rejected` en el procesamiento asíncrono, el webhook IPN registrará el detalle del rechazo en la tabla `Pago` y dejará el pedido en estado `PENDIENTE` para que el cliente pueda reintentar con otro medio de pago sin perder su orden.
