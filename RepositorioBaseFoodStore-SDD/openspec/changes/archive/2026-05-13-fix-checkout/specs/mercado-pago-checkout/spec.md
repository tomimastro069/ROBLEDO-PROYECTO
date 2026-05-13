## MODIFIED Requirements

### Requirement: Procesamiento de Checkout con MercadoPago
El sistema MUST permitir la creación de preferencias de pago e integrar el SDK de MercadoPago en el cliente bajo cumplimiento PCI DSS SAQ-A, incorporando un modo Sandbox local cuando se detecten tokens de prueba.

#### Scenario: Creación exitosa de preferencia
- **WHEN** un cliente autenticado solicita el pago de un pedido existente en estado PENDIENTE
- **THEN** el backend MUST generar e inyectar una clave de idempotencia UUID única y retornar el identificador de preferencia tomando el monto inmutable desde las líneas del pedido

#### Scenario: Intercepción Sandbox ante credenciales de prueba
- **WHEN** el backend detecta que la variable de entorno `MP_ACCESS_TOKEN` inicia con la cadena `"TEST-"`
- **THEN** el sistema MUST eludir la petición de red externa hacia la API real de MercadoPago y retornar una preferencia simulada con identificador mock y un `init_point` dirigido a la vista de retorno local

### Requirement: Recepción y Orquestación de Webhooks IPN
El sistema MUST escuchar las notificaciones asíncronas de MercadoPago y procesar el avance del pedido de forma transaccional, con soporte para simulación local.

#### Scenario: Confirmación atómica de pago aprobado
- **WHEN** el webhook recibe una notificación con estado approved para un pago pendiente
- **THEN** el sistema MUST orquestar de forma atómica mediante la Unidad de Trabajo (Unit of Work) el avance de la máquina de estados del pedido a CONFIRMADO y registrar el evento en el historial de auditoría append-only

#### Scenario: Procesamiento Sandbox de notificación simulada
- **WHEN** el webhook recibe una notificación simulada en modo Sandbox (token de prueba)
- **THEN** el sistema MUST omitir la validación externa y la firma criptográfica en caso de ausencia de secreto, procesando la aprobación del pago de manera atómica
