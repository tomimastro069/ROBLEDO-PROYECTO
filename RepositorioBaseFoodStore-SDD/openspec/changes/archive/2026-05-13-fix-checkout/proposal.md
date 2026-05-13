## Why

La implementación actual asume que todos los pagos fluyen obligatoriamente a través del SDK de MercadoPago en modo en vivo, provocando rechazos del tipo `502 Bad Gateway` en entornos locales al utilizar credenciales de prueba (`TEST-xxxx`). Además, existe una discrepancia crítica con la especificación técnica canónica del sistema (v5.0), la cual exige la existencia del catálogo `FormaPago` para soportar de forma nativa flujos offline mediante `EFECTIVO` y `TRANSFERENCIA`, permitiendo a los gestores avanzar manualmente los pedidos constatados.

## What Changes

- Creación e inyección del modelo de base de datos de catálogo `FormaPago` alineado con la especificación técnica.
- Inserción de seed data obligatorio para inicializar las tres formas de pago nativas (`MERCADOPAGO`, `EFECTIVO`, `TRANSFERENCIA`).
- Bifurcación en el caso de uso de creación de pagos para evitar la invocación externa al SDK de MercadoPago cuando el cliente selecciona métodos offline (`EFECTIVO` o `TRANSFERENCIA`), registrando el pago en estado `pending`.
- Implementación del Patrón Sandbox (Dev Mode Bypass) interceptando la salida de red del SDK de MercadoPago cuando el token posea el prefijo `"TEST-"`, retornando mock URLs exitosas para destrabar el desarrollo y las pruebas E2E locales.

## Capabilities

### New Capabilities
- `offline-payments`: Soporte nativo para flujos de pago desacoplados de pasarelas externas mediante Efectivo y Transferencia bancaria, delegando la confirmación al avance de la máquina de estados por parte del personal autorizado.

### Modified Capabilities
- `mercado-pago-checkout`: Incorporación de soporte Sandbox para emular el ciclo de vida de la preferencia y del Webhook IPN de MercadoPago en entornos locales desprovistos de conectividad comercial en vivo.

## Impact

- **Modelos de Base de Datos**: Creación de la tabla `FormaPago` y clave foránea desde la tabla de Pedidos.
- **Módulo Pagos**: Intercepción en `pagos/router.py` y `webhook_mercadopago.py` para aplicar el modo Sandbox ante tokens de prueba.
- **Manejo de Transacciones**: Preservación estricta de los límites del Unit of Work (UoW) garantizando rollback limpio ante cualquier eventualidad.
