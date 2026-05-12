# Dominio Especial: Pagos con MercadoPago

## Integración de Checkout API (Orders)
El sistema integra de forma nativa la pasarela de pagos de MercadoPago en su modalidad de **Checkout API**, permitiendo procesar transacciones directamente dentro del flujo de la aplicación web sin desviar al cliente hacia páginas de cobro externas.

### Cumplimiento de Normativa PCI DSS (SAQ-A)
Para garantizar la máxima seguridad financiera y eximir a la infraestructura de Food Store de auditorías complejas sobre el manejo de números de tarjeta de crédito/débito, se implementa el SDK de JavaScript en el cliente (`@mercadopago/sdk-react`). Los campos del formulario de tarjeta se renderizan dentro de iframes seguros controlados exclusivamente por los servidores de MercadoPago. El servidor de Food Store únicamente entra en contacto con un token de un solo uso (`card_token`) completamente opaco.

### Gestión de Idempotencia
Cada solicitud de cobro originada en el backend hacia la API de MercadoPago viaja con una cabecera única generada en base de datos mediante la librería `uuid` nativa de Python, asignada al campo `idempotency_key`. Esta medida neutraliza de forma absoluta el riesgo de cobros duplicados accidentales causados por dobles clics en la interfaz o reintentos automáticos de red ante *timeouts*.

## Mapeo de Estados
La tabla `Pago` registra las actualizaciones asíncronas reportadas por el Webhook IPN, traduciendo los estados nativos de la pasarela al ciclo de vida del pedido en Food Store:

| Estado MP (`mp_status`) | Detalle Típico | Acción Automática en Base de Datos |
| :--- | :--- | :--- |
| `approved` | `accredited` | El webhook orquesta a través de la capa `Unit of Work` el avance inmediato y atómico del pedido asociado desde el estado `PENDIENTE` hacia `CONFIRMADO`. |
| `pending` | `pending_contingency` / `pending_review_manual` | El pago ha sido iniciado (ej. generación de cupón en efectivo en Rapipago/Pago Fácil). El pedido permanece inalterado en estado `PENDIENTE`. |
| `rejected` | `cc_rejected_insufficient_amount` / `cc_rejected_bad_filled_security_code` | Cobro denegado. Se actualiza el registro en la tabla `Pago` con el motivo para mostrarlo en la UI. El pedido sigue en `PENDIENTE` habilitando reintentos limpios. |
| `cancelled` | `expired` | El cupón de pago en efectivo expiró sin ser abonado. Se habilita la cancelación de la orden. |

## Tarjetas de Prueba (Sandbox Oficial)
Para ejecutar pruebas end-to-end (E2E) en entornos de desarrollo local, se deben utilizar los siguientes números de tarjeta provistos por el entorno Sandbox de MercadoPago:

- **Visa (Aprobada)**: `4509 9535 6623 3704` — CVV: `123` — Vencimiento: `11/25`
- **American Express (Aprobada)**: `3714 496353 98431` — CVV: `1234` — Vencimiento: `11/25`
- **Visa (Rechazada por fondos insuficientes)**: `4000 0000 0000 0002` — CVV: `123` — Vencimiento: `11/25`
