## Why

Actualmente, la integración de pagos con MercadoPago y la página de checkout son esqueletos mínimos o placeholders. El router de pagos crea preferencias con un precio de prueba fijado en `1.0`, el webhook IPN se limita a hacer `print()` del payload sin procesar las confirmaciones, y el frontend carece por completo de la interfaz de pago y las pantallas de resultado. Es imperativo implementar el flujo real transaccional de cobro para que las compras se traduzcan en pedidos pagados y confirmados en el sistema de manera íntegra, segura y robusta.

## What Changes

- **Integración Segura en el Cliente**: Implementación de la página de Checkout en React integrando el SDK oficial de MercadoPago (`@mercadopago/sdk-react`) para garantizar el cumplimiento de la normativa PCI DSS (SAQ-A) mediante iframes de tokenización.
- **Creación de Preferencias Transaccionales**: Modificación de `backend/pagos/router.py` para inyectar una clave de idempotencia única (UUID) y vincular el precio real inmutable desde las líneas del pedido.
- **Persistencia de Pagos**: Creación del modelo de base de datos `Pago` para registrar cada transacción originada, permitiendo trazabilidad y conciliación.
- **Procesamiento de Webhooks IPN**: Implementación de la lógica completa en `/webhooks/mercadopago` validando el origen, verificando la idempotencia y orquestando de forma atómica el avance del pedido de `PENDIENTE` a `CONFIRMADO` a través de la Unidad de Trabajo (`Unit of Work`) y la Máquina de Estados (FSM).
- **Flujos de Resultado UI**: Creación de las páginas de estado para redirección post-pago (`/pago/exito`, `/pago/error`, `/pago/pendiente`).

## Capabilities

### New Capabilities
- `mercado-pago-checkout`: Integración de pasarela de pagos con MercadoPago Checkout API (Orders), tokenización de tarjetas bajo PCI DSS SAQ-A, persistencia del modelo de pago, manejo de idempotencia y escucha/procesamiento de notificaciones Webhook IPN para el avance de la FSM del pedido.

### Modified Capabilities
- `orders-service`: Se amplía para contemplar la interacción asíncrona del Webhook de pagos sobre la orquestación de la FSM (transición de `PENDIENTE` a `CONFIRMADO`) y el uso de transacciones con la capa `Unit of Work`.

## Impact

- **Modelos y Base de Datos**: Nueva tabla `pago` vía migración de Alembic con su respectivo plan de rollback.
- **Backend APIs**: `backend/pagos/router.py` y `backend/app/api/webhook_mercadopago.py`.
- **Frontend UI**: Nueva página de checkout e interfaces de confirmación/error bajo el enrutador de React.
- **Dependencias**: Confirmación del uso del SDK de MP en backend y `@mercadopago/sdk-react` en frontend.
