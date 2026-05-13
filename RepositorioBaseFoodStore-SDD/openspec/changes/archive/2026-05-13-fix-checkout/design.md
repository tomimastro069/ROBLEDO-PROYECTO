## Context

El sistema cuenta con el dominio de pedidos gestionado por una Máquina de Estados (FSM) y transacciones atómicas mediante la Unidad de Trabajo (`Unit of Work`). Sin embargo, el módulo de pagos fue acoplado de manera rígida al SDK de MercadoPago, asumiendo que todo pedido debe originar una preferencia externa online. Esto rompió el cumplimiento de la especificación técnica base (v5.0) que exige el soporte offline nativo a través del catálogo `FormaPago` (`MERCADOPAGO`, `EFECTIVO`, `TRANSFERENCIA`), y causó bloqueos de desarrollo local (`502 Bad Gateway`) ante la ausencia de credenciales comerciales en vivo.

## Goals / Non-Goals

**Goals:**
- Mapear la entidad catálogo `FormaPago` en SQLModel e integrarla mediante clave foránea en la tabla `orders`.
- Diseñar la ramificación del flujo transaccional en `pagos/router.py`: delegar al SDK de MercadoPago exclusivamente para la forma de pago `MERCADOPAGO`, y registrar de manera inmediata transacciones en estado `pending` para `EFECTIVO` y `TRANSFERENCIA`.
- Diseñar el patrón Dev Mode Bypass (Sandbox) interceptando la salida del SDK de MercadoPago ante tokens con prefijo `"TEST-"`, devolviendo respuestas simuladas que eviten fallos de pasarela.
- Garantizar que los límites transaccionales del Unit of Work (`AppUnitOfWork`) resguarden la consistencia del pedido y del pago en una única transacción atómica en base de datos.
- Proporcionar la arquitectura de testing y estrategia de mocks aislando el SDK externo.

**Non-Goals:**
- Implementar integraciones directas con las APIs bancarias para conciliación automática de transferencias (fuera de alcance, verificación manual por el gestor).

## Decisions

### 1. Entidad Catálogo FormaPago y Relación ER
- **Decisión**: Mapear la entidad `FormaPago` con los campos `codigo: str` (PK semántica) y `habilitado: bool` en un nuevo archivo de modelos o en `orders/models.py`. Se relacionará como FK nula o requerida en la entidad `Order`.
- **Racional**: Cumple de forma estricta con el Entity-Relationship Pattern del ERD v5. Permite deshabilitar formas de pago en caliente sin alterar pedidos históricos.

### 2. Bifurcación Transaccional y Límites UoW en Router de Pagos
- **Decisión**: Al recibir `POST /api/v1/pagos/crear`, el router abrirá el gestor de contexto `with uow:`. Consultará la forma de pago del pedido. Si es `EFECTIVO` o `TRANSFERENCIA`, insertará un registro en la tabla `Pago` con `mp_status="pending"` y confirmará la transacción con `uow.commit()`. El pedido permanecerá en estado `PENDIENTE`.
- **Racional**: Garantiza que los flujos offline no intenten contactar servidores externos y mantengan una trazabilidad unificada en la misma tabla de pagos.

### 3. Patrón Sandbox (Dev Mode Bypass) para el SDK de MercadoPago
- **Decisión**: Envolver la invocación a `sdk.preference().create()` y `sdk.payment().get()` en una factoría o bloque condicional. Si `os.getenv("MP_ACCESS_TOKEN", "")` inicia con `"TEST-"`, se omite la llamada de red HTTP externa y se devuelve una estructura de diccionario mock con un `preference_id` ficticio y un `init_point` que dirija a la UI local.
- **Racional**: Destraba instantáneamente el desarrollo y las pruebas E2E locales sin requerir túneles ngrok ni tokens reales.

### 4. Transiciones de Estado FSM para Pagos Offline
- **Decisión**: El avance de `PENDIENTE` a `CONFIRMADO` para pedidos abonados con Efectivo o Transferencia será accionado de manera manual por los roles `ADMIN` o `PEDIDOS` consumiendo `PATCH /api/v1/pedidos/{id}/estado`.
- **Transiciones**:
  $$\text{PENDIENTE} \xrightarrow{\text{PATCH /estado (Admin/Pedidos)}} \text{CONFIRMADO (Dispara decremento de stock atómico)}$$

### 5. Estrategia de Mocks y Testing
- **Decisión**: Se implementarán pruebas unitarias inyectando un mock sobre la clase `mercadopago.SDK` utilizando `unittest.mock` para verificar que la lógica del router bifurque correctamente según el código de la forma de pago.

## Risks / Trade-offs

- **Riesgo de Atraso en Confirmación de Transferencias** $\rightarrow$ **Mitigación**: El sistema preserva el inventario disponible sin restarlo hasta que el gestor avanza manualmente el pedido a `CONFIRMADO`, evitando el secuestro de stock por pedidos no pagados.
- **Riesgo de Inconsistencia de Claves Foráneas en Migración** $\rightarrow$ **Mitigación**: El script de seed o la migración de Alembic insertará los registros catálogo por defecto antes de aplicar la restricción de clave foránea en la tabla de pedidos.
