# Offline Payments Specifications

## Functional Requirements

### Requirement: Registro de Pagos Offline Nativos
El sistema MUST soportar formas de pago desacopladas de pasarelas externas basadas en el catálogo `FormaPago`, específicamente `EFECTIVO` y `TRANSFERENCIA`.

#### Scenario: Registro inmediato de cobro pendiente
- **WHEN** un cliente confirma un pedido utilizando la forma de pago `EFECTIVO` o `TRANSFERENCIA`
- **THEN** el backend MUST persistir de forma inmediata un registro en la tabla de Pagos con estado nativo `pending` sin contactar pasarelas de red externas, manteniendo el pedido en estado PENDIENTE

### Requirement: Avance Manual de Pedidos Pagados Offline
El sistema MUST permitir a los gestores avanzar manualmente el ciclo de vida de los pedidos constatados de manera física o bancaria.

#### Scenario: Confirmación manual de pedido verificado
- **WHEN** un usuario con rol ADMIN o PEDIDOS actualiza el estado de un pedido abonado offline hacia CONFIRMADO
- **THEN** el sistema MUST validar la máquina de estados y aplicar atómicamente la transición y el decremento de inventario correspondiente
