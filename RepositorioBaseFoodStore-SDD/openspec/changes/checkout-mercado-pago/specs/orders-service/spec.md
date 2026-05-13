## ADDED Requirements

### Requirement: Integración de Pagos en la Orquestación de Pedidos
La capa de servicio de pedidos MUST proveer los métodos transaccionales para que el servicio de pagos actualice de forma atómica el estado del pedido ante confirmaciones de pasarela.

#### Scenario: Transición orquestada por Webhook de MercadoPago
- **WHEN** se invoca la confirmación de pago exitoso desde el listener de notificaciones IPN
- **THEN** la capa de servicio MUST verificar que el pedido se encuentre en estado PENDIENTE y avanzar de forma segura a CONFIRMADO dentro de los límites de la Unidad de Trabajo (UoW)
