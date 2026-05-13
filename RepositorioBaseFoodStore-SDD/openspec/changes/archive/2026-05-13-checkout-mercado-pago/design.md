## Context

El sistema cuenta con un flujo funcional para la creación de pedidos en estado inicial `PENDIENTE` mediante la Unidad de Trabajo (`Unit of Work`). Sin pasarela conectada, no existe forma automatizada de concretar el pago y avanzar el ciclo de vida del pedido de forma segura. La pasarela de MercadoPago Checkout API (Orders) requiere un manejo preciso para no violar normativas de seguridad (PCI DSS), evitar condiciones de carrera o duplicaciones de confirmación ante notificaciones de red (IPN webhooks), y aislar el estado en el cliente (Zustand) y servidor.

## Goals / Non-Goals

**Goals:**
- Diseñar el modelo de datos `Pago` en SQLModel con claves foráneas hacia `Pedido` y trazabilidad del identificador de preferencia y estado de MercadoPago.
- Orquestar la creación de preferencias inyectando una `idempotency_key` única e inmutable y tomando el monto total calculado desde las líneas inmutables del pedido transaccional.
- Diseñar la recepción y validación de notificaciones Webhook IPN garantizando que el avance del pedido a `CONFIRMADO` ocurra dentro de los límites transaccionales de la Unidad de Trabajo (`Unit of Work`), disparando correctamente el historial de auditoría append-only (**RN-03**).
- Diseñar la capa UI de Checkout utilizando iframes seguros del SDK de MercadoPago (`@mercadopago/sdk-react`) y enrutamiento con vistas de resultado.
- Establecer la arquitectura de testing con mocks para el SDK de MP y pruebas unitarias/integración de la lógica del webhook.

**Non-Goals:**
- Implementar pasarelas de pago adicionales (ej. Stripe, PayPal).
- Envío automatizado de facturas fiscales electrónicas (AFIP) en esta fase.

## Decisions

### 1. Tokenización en Cliente bajo PCI DSS SAQ-A
- **Decisión**: Utilizar `@mercadopago/sdk-react` en el frontend para renderizar el formulario de tarjeta dentro de iframes provistos por MercadoPago.
- **Racional**: Evita que los datos sensibles de tarjetas pasen por la memoria o red del servidor FastAPI, reduciendo drásticamente el alcance de auditoría de seguridad. El backend solo procesará el token opaco resultante.
- **Alternativas consideradas**: Formulario nativo con envío directo a nuestra API (descartado por altísimo riesgo de cumplimiento normativo y filtrado de datos).

### 2. Límites Transaccionales del Webhook en la Unidad de Trabajo (UoW)
- **Decisión**: El endpoint asíncrono `/webhooks/mercadopago` invocará un servicio de dominio que abrirá el gestor de contexto `async with uow:` (o su equivalente síncrono según la implementación base del UoW). Todas las lecturas del pedido, verificación de idempotencia, inserción del registro en `Pago`, actualización de la FSM a `CONFIRMADO` y la inserción en `HistorialEstadoPedido` ocurrirán en una única transacción atómica.
- **Racional**: Si ocurre un error de concurrencia o caída de red en medio de la actualización, la base de datos completa ejecuta un rollback limpio sin dejar el pedido en un estado inconsistente.
- **Transiciones de Estado FSM**:
  $$\text{PENDIENTE} \xrightarrow{\text{IPN: approved}} \text{CONFIRMADO}$$
  $$\text{PENDIENTE} \xrightarrow{\text{IPN: rejected}} \text{PENDIENTE (Registra motivo en Pago, permite reintento)}$$

### 3. Modelo Relacional y Persistencia del Pago
- **Decisión**: Crear la entidad `Pago` mapeando `id`, `pedido_id` (FK), `preference_id`, `idempotency_key` (UUID único), `status` y `payment_id` (de MP).
- **Racional**: Permite conciliar pagos externos con los pedidos internos y provee un bloqueo de unicidad (`UNIQUE` en `idempotency_key` y `payment_id`) a nivel base de datos.

### 4. Estrategia de Mocks y Arquitectura de Testing
- **Decisión**: Aislar el SDK de MercadoPago en los tests unitarios inyectando una clase adaptadora o aplicando `unittest.mock.patch` sobre `mercadopago.SDK`. Se escribirán tests para el servicio del Webhook simulando payloads válidos (`approved`), firmas inválidas, y eventos duplicados para comprobar la idempotencia.

## Risks / Trade-offs

- **Riesgo de Notificaciones Duplicadas o Fuera de Orden (IPN)** $\rightarrow$ **Mitigación**: La capa de servicio consultará primero si el `payment_id` ya fue procesado exitosamente o si el pedido ya se encuentra en estado `CONFIRMADO` o superior. Si es así, retornará HTTP 200 OK inmediatamente sin re-ejecutar transacciones (Idempotencia estricta).
- **Riesgo de Caída del Servidor de Food Store durante IPN** $\rightarrow$ **Mitigación**: MercadoPago implementa reintentos exponenciales automáticos. Al no confirmarse el pedido localmente, el cliente verá el estado pendiente en su UI hasta que el servidor reciba el reintento y complete la FSM.
