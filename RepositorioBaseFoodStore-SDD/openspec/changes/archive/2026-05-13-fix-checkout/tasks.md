## 1. Base de Datos y Catálogos Backend

- [x] 1.1 Crear entidad catálogo `FormaPago` en `backend/orders/models.py` (o módulo de dominio unificado) con `codigo` y `habilitado`.
- [x] 1.2 Agregar inyección de seed data en `backend/app/db/seed.py` para cargar los registros iniciales obligatorios (`MERCADOPAGO`, `EFECTIVO`, `TRANSFERENCIA`).
- [x] 1.3 Generar migración de Alembic para crear la tabla de formas de pago e incluir plan de rollback.

## 2. Lógica Transaccional y Modo Sandbox (Router & Webhook)

- [x] 2.1 Refactorizar endpoint `POST /api/v1/pagos/crear` en `backend/pagos/router.py` para aplicar bifurcación: cobros con `EFECTIVO` o `TRANSFERENCIA` registran el pago como `pending` y retornan 201 de forma inmediata.
- [x] 2.2 Implementar intercepción Sandbox (Dev Mode Bypass) en `backend/pagos/router.py` ante tokens de prueba (`TEST-`) para retornar un identificador de preferencia y vista exitosa simulados.
- [x] 2.3 Adaptar `backend/app/api/webhook_mercadopago.py` para procesar notificaciones simuladas en Sandbox evadiendo validación externa de red cuando aplique.

## 3. Pruebas Unitarias y Mocks (Strict TDD)

- [x] 3.1 Añadir pruebas unitarias en `backend/tests/` comprobando que la creación de pago por transferencia no invoque al SDK de MercadoPago.
- [x] 3.2 Añadir prueba unitaria comprobando que el modo Sandbox retorne correctamente las URLs simuladas sin fallos de pasarela.
