## 1. Base de Datos y Modelos Backend

- [x] 1.1 Crear modelo SQLModel `Pago` en `backend/pagos/models.py` (o archivo unificado) con mapeo relacional hacia `Pedido` y restricciones de unicidad.
- [x] 1.2 Generar y aplicar migración de Alembic para la tabla `pago` documentando el comando de rollback.

## 2. Lógica Transaccional Backend (Service & Router)

- [x] 2.1 Modificar capa Router en `backend/pagos/router.py` para inyectar `idempotency_key` persistida y consultar el precio inmutable del pedido transaccional.
- [x] 2.2 Implementar capa Service en `backend/orders/service.py` (o dominio equivalente) para proveer el método de confirmación atómica por pago en la Unidad de Trabajo (`Unit of Work`).
- [x] 2.3 Implementar lógica de Webhook IPN en `backend/app/api/webhook_mercadopago.py` validando firmas e invocando el avance de estado de `PENDIENTE` a `CONFIRMADO` de forma idempotente.

## 3. Pruebas Unitarias y de Integración (Strict TDD)

- [x] 3.1 Escribir tests unitarios con pytest mockeando el SDK de MercadoPago y validando el rechazo de firmas inválidas en el Webhook.
- [x] 3.2 Escribir tests de integración comprobando que notificaciones IPN duplicadas respeten la idempotencia sin duplicar inserciones de auditoría.

## 4. Frontend UI y Conexión de Checkout

- [x] 4.1 Instalar e integrar `@mercadopago/sdk-react` en `package.json`.
- [x] 4.2 Crear página y feature de Checkout (`CheckoutPage.tsx`) implementando iframes seguros para tokenización bajo PCI DSS SAQ-A.
- [x] 4.3 Crear páginas de redirección y feedback (`PagoExitoPage.tsx`, `PagoErrorPage.tsx`, `PagoPendientePage.tsx`) registradas en el Router.
