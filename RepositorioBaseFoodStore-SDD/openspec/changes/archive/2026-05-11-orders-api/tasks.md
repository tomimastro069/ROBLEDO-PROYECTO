# TASKS: Orders API (Change #20)

## Phase 1: Preparation & Schemas
- [x] 1.1. Create `backend/orders/schemas.py` with `OrderCreate`, `OrderRead`, `OrderAdminRead`, and `StateChangeRequest`.
- [x] 1.2. Define `PaginatedResponse` for orders to match project standards.

## Phase 2: Test Infrastructure (TDD)
- [x] 2.1. Create `backend/tests/test_orders_api.py`. (Overwritten `test_orders_routes.py`)
- [x] 2.2. Implement failing test: `test_create_order_success`.
- [x] 2.3. Implement failing test: `test_cancel_order_unauthorized` (RN-RB05).
- [x] 2.4. Implement failing test: `test_advance_state_fsm_violation` (RN-FS01).

## Phase 3: Core Implementation
- [x] 3.1. Implement `POST /orders` endpoint using `OrderService.create_order`.
- [x] 3.2. Implement `GET /orders/{id}` with ownership validation.
- [x] 3.3. Implement `GET /orders` with user-specific filtering.
- [x] 3.4. Implement `PATCH /orders/{id}/cancel` enforcing `reason` and `RN-FS08`.

## Phase 4: Administrative Features
- [x] 4.1. Implement `GET /admin/orders` for `Role.PEDIDOS` and `Role.ADMIN`.
- [x] 4.2. Implement `PATCH /admin/orders/{id}/status` for state progression.

## Phase 5: Verification & Polish
- [x] 5.1. Run all tests: `python -m pytest backend/tests/test_orders_api.py`.
- [x] 5.2. Verify correlation ID propagation in logs.
- [x] 5.3. Document API in Swagger/OpenAPI.
