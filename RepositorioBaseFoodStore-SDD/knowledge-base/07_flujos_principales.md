# Flujos Principales

## Flujo de Creación de Pedido (UoW y Snapshot)
La creación de una orden de compra representa la transacción más crítica del sistema, involucrando múltiples inserciones dependientes que deben ejecutarse bajo garantías estrictas de atomicidad (ACID) orquestadas por el **Unit of Work**.

```
Cliente         Router          Service          Unit of Work         PostgreSQL
   |              |                |                  |                    |
   |-- POST/pedidos(body)          |                  |                    |
   |              |-- with UnitOfWork() as uow:       |                    |
   |              |   |-- crear_pedido(uow, body)     |                    |
   |              |                |-- get_by_id() -->|-- SELECT producto  |
   |              |                |   (valida stock) |                    |
   |              |                |-- calcula total  |                    |
   |              |                |-- create(pedido)>|-- INSERT Pedido    |
   |              |                |-- flush() ------>|                    |
   |              |                |-- crea Detalles->|-- INSERT Detalles  |
   |              |                |   (xN con snaps) |                    |
   |              |                |-- crea Historial>|-- INSERT Historial |
   |              |<-- retorna req.|                  |   (desde=NULL)     |
   |              |-- __exit__ sin excepciones ------>|-- COMMIT atómico ->|
   |<-- HTTP 201 -|                                   |                    |
```

**Secuencia paso a paso:**
1. El `Router` recibe la petición HTTP `POST /api/v1/pedidos` con el cuerpo validado por el esquema `CrearPedidoRequest` de Pydantic.
2. El `Router` inicializa el gestor de contexto del `Unit of Work` (`with UnitOfWork() as uow:`) e invoca el método del servicio `service.crear_pedido(uow, body, usuario_id)`.
3. El `Service` itera sobre los ítems del carrito. Para cada uno, consulta el repositorio de productos inyectado en el UoW (`uow.productos.get_by_id()`) y verifica que `disponible = true` y que el stock sea suficiente.
4. El `Service` calcula estáticamente el costo total sumando el producto de `precio_base` por la cantidad solicitada de cada ítem, sumando el valor fijo de `costo_envio`.
5. El `Service` genera la cabecera de la orden y ejecuta `uow.pedidos.create(pedido)` seguido de un `uow.flush()` para obtener el identificador primario autogenerado (`pedido.id`) de la base de datos sin confirmar la transacción.
6. El `Service` inserta de forma masiva los registros en `DetallePedido`, copiando inmutablemente el nombre y precio en los campos snapshot (`nombre_snapshot`, `precio_snapshot`) y persistiendo las personalizaciones en el array nativo (`INTEGER[]`).
7. El `Service` inserta el primer evento en `HistorialEstadoPedido` estableciendo `estado_desde = None` y `estado_hasta = 'PENDIENTE'` cumpliendo con la regla **RN-02**.
8. Al finalizar el bloque sin excepciones, el método `__exit__` del UoW invoca automáticamente `session.commit()`, persistiendo todas las inserciones de forma totalmente atómica. Si ocurriera cualquier error, se ejecuta `session.rollback()`.

## Flujo de Pago Integrado (MercadoPago Checkout API)
Este flujo garantiza que los datos sensibles de tarjetas de crédito/débito jamás toquen los servidores de la aplicación, delegando el cumplimiento de PCI DSS SAQ-A al SDK de JavaScript.

```
Cliente / Navegador        Backend (FastAPI)       MercadoPago API
        |                          |                      |
        |-- Renderiza Card JS SDK  |                      |
        |-- Ingresa Tarjeta        |                      |
        |-- Tokeniza en cliente ------------------------->|
        |<-- Retorna card_token --------------------------|
        |-- POST /pagos/crear(token)                      |
        |                          |-- Genera idempotency |
        |                          |   key (UUID)         |
        |                          |-- Envíos de cobro -->|
        |                          |<-- Retorna mp_id ----|
        |                          |-- INSERT Pago (UoW)  |
        |<-- HTTP 201 (Pendiente) -|                      |
        |                          |                      | (Procesamiento)
        |                          |<-- Webhook IPN ------|
        |                          |    (topic=payment)   |
        |                          |-- Valida y avanza    |
        |                          |   Pedido a CONFIRMADO|
```

**Secuencia paso a paso:**
1. El frontend renderiza el formulario de pago utilizando `@mercadopago/sdk-react`.
2. El cliente ingresa los datos de su tarjeta directamente en los iframes seguros de MercadoPago.
3. MercadoPago intercepta los datos, los tokeniza y devuelve un `card_token` de un solo uso al frontend.
4. El frontend envía este token opaco al backend llamando a `POST /api/v1/pagos/crear`.
5. El backend genera de forma determinista o aleatoria segura una clave de idempotencia única tipo UUID (`idempotency_key`) para prevenir dobles cobros ante reintentos por latencia.
6. El backend consume la API REST de MercadoPago a través del SDK de Python enviando el monto, token y referencia externa (`external_reference` mapeada al UUID o ID del pedido).
7. MercadoPago responde de forma síncrona con el identificador de transacción (`mp_payment_id`) y un estado inicial (típicamente `pending` o `in_process`).
8. El backend inserta un registro en la tabla `Pago` asociando los identificadores y responde al cliente.
9. De forma asíncrona, los servidores de MercadoPago emiten una notificación push (Webhook IPN) hacia `POST /api/v1/pagos/webhook`.
10. El backend valida la firma o consulta el estado real del pago, y si el estado es `approved`, orquesta a través del UoW el avance automático del pedido hacia el estado `CONFIRMADO`.
