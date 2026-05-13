## ADDED Requirements

### Requirement: Procesamiento de Checkout con MercadoPago
El sistema MUST permitir la creación de preferencias de pago e integrar el SDK de MercadoPago en el cliente bajo cumplimiento PCI DSS SAQ-A.

#### Scenario: Creación exitosa de preferencia
- **WHEN** un cliente autenticado solicita el pago de un pedido existente en estado PENDIENTE
- **THEN** el backend MUST generar e inyectar una clave de idempotencia UUID única y retornar el identificador de preferencia tomando el monto inmutable desde las líneas del pedido

### Requirement: Recepción y Orquestación de Webhooks IPN
El sistema MUST escuchar las notificaciones asíncronas de MercadoPago y procesar el avance del pedido de forma transaccional.

#### Scenario: Confirmación atómica de pago aprobado
- **WHEN** el webhook recibe una notificación con estado approved para un pago pendiente
- **THEN** el sistema MUST orquestar de forma atómica mediante la Unidad de Trabajo (Unit of Work) el avance de la máquina de estados del pedido a CONFIRMADO y registrar el evento en el historial de auditoría append-only
