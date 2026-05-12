# Tasks: Orders Service Implementation

## Phase 1: Foundation & Data Persistence (Infrastructure)

- [X] 1.1 Create `backend/orders/models.py` with SQLModel Order, OrderItem, OrderStatus entities
- [X] 1.2 Create `backend/orders/schemas.py` with Pydantic request/response schemas (OrderCreate, OrderUpdate, OrderResponse)
- [X] 1.3 Create database migration in `backend/alembic/versions/` for orders and order_items tables with indices on user_id, status, created_at
- [X] 1.4 Create `backend/orders/repository.py` with OrderRepository class for CRUD operations via SQLModel
- [X] 1.5 Create `backend/orders/exceptions.py` with domain exceptions (OrderNotFound, InvalidStatusTransition, InsufficientStock)

## Phase 2: Core Business Logic & Validation (Implementation)

- [X] 2.1 Create `backend/orders/state_machine.py` with OrderStateMachine class enforcing state transitions (Draft → Submitted → Processing → Completed/Cancelled)
- [X] 2.2 Create `backend/orders/service.py` with OrderService implementing create, retrieve, update, cancel, and list operations
- [X] 2.3 Add validation logic in OrderService to call external services (inventory, catalog) via HTTP clients
- [X] 2.4 Create `backend/orders/validators.py` with business rule validators (product availability, price validation, payment method validation)
- [X] 2.5 Create `backend/orders/events.py` with event DTOs (OrderCreated, OrderUpdated, OrderCancelled, OrderSubmitted)
- [X] 2.6 Implement event publishing logic in OrderService to emit events to RabbitMQ message broker

## Phase 3: API Integration & Wiring (Endpoints)

- [x] 3.1 Create `backend/orders/routes.py` with FastAPI routes: POST /orders (create), GET /orders/{id} (retrieve), GET /orders (list by user_id with pagination/filters)
- [x] 3.2 Add PATCH /orders/{id} route for status updates with state machine validation
- [x] 3.3 Add DELETE /orders/{id} route for order cancellation with inventory/payment reversal
- [x] 3.4 Implement JWT authentication & authorization middleware in routes (users manage own, admins access all)
- [x] 3.5 Create `backend/orders/__init__.py` and register routes in main FastAPI app at `/api/v1/orders`
- [x] 3.6 Implement correlation ID tracking in all endpoints for request tracing

## Phase 4: External Service Integration (Orchestration)

- [x] 4.1 Create `backend/orders/clients/inventory_client.py` to call inventory service for stock verification and deduction
- [x] 4.2 Create `backend/orders/clients/catalog_client.py` to validate product prices via catalog service
- [x] 4.3 Create `backend/orders/clients/payment_client.py` to authorize/refund payments via payment service
- [x] 4.4 Implement retry logic (max 2 attempts, 3-second timeout) with circuit breaker pattern for all external calls
- [x] 4.5 Create `backend/orders/clients/event_publisher.py` to publish OrderCreated, OrderSubmitted, OrderCancelled events to RabbitMQ

## Phase 5: Testing (Unit & Integration)

- [x] 5.1 Create `backend/tests/test_orders_models.py` - test Order/OrderItem entity validations
- [x] 5.2 Create `backend/tests/test_orders_state_machine.py` - test state transitions and invalid transitions
- [x] 5.3 Create `backend/tests/test_orders_service.py` - test create, retrieve, update, cancel operations
- [x] 5.4 Create `backend/tests/test_orders_validators.py` - test inventory, price, and payment validations
- [x] 5.5 Create `backend/tests/test_orders_routes.py` - test POST /orders (success/conflict), GET /orders/{id}, PATCH status, DELETE cancel
- [x] 5.6 Create `backend/tests/test_orders_integration.py` - test full flow: create → validate → submit → complete with mock external services
- [x] 5.7 Add test for concurrent order submissions (stress test with 10+ simultaneous requests)
- [x] 5.8 Add test for idempotency: duplicate OrderCreated events should not create duplicate orders

## Phase 6: Documentation & Monitoring

- [x] 6.1 Create `docs/orders-api.md` with OpenAPI 3.0 spec and endpoint documentation
- [x] 6.2 Add structured logging to OrderService with correlation IDs for request tracing
- [x] 6.3 Create Prometheus metrics for: orders_created_total, order_processing_duration_ms, order_errors_total
- [x] 6.4 Add health check endpoint GET /orders/health returning service status and dependencies health
- [x] 6.5 Document state machine transitions in `docs/orders-state-machine.md`
- [x] 6.6 Update `backend/README.md` with orders-service setup and configuration instructions
