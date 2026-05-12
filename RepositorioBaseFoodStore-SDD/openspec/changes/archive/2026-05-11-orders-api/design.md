# TECHNICAL DESIGN: Orders API (Change #20)

## Architecture Overview
The Orders API will be implemented as a thin controller layer in FastAPI, delegating all complex business logic and state transitions to the `OrderService`. It will leverage FastAPI dependencies for RBAC and Traceability.

## Component Design

### 1. Router Layout
- **Path**: `backend/orders/routes.py`
- **Prefix**: `/api/v1`
- **Tags**: `["Orders"]`

### 2. Dependency Injection
- `get_order_service`: Factory to initialize `OrderService` with the current DB session and `correlation_id`.
- `get_correlation_id`: Capture `x-correlation-id` from headers or generate a new one.

### 3. FSM Integration
Instead of generic CRUD updates, we will implement specialized endpoints for state changes:
- `/cancel`: Maps to `order_service.cancel_order()`.
- `/status`: Maps to `order_service.advance_state()`.
This prevents clients from setting arbitrary states.

### 4. DTO Strategy (Pydantic)
- `OrderCreate`: Input for creation (US-035).
- `OrderRead`: Standard output for users.
- `OrderAdminRead`: Extended output for admins (includes user info and detailed history).
- `StateChangeRequest`: For cancellation and status updates (includes `reason`).

## Technical Constraints
- **Atomicity**: All state-changing endpoints must use a single Unit of Work transaction.
- **Traceability**: The `correlation_id` MUST be passed to every service call.
- **Performance**: Listing endpoints must use optimized joins to avoid N+1 queries when fetching items and snapshots.

## Cross-Cutting Concerns
- **Error Mapping**: Map `DomainException` sub-classes from the service layer to appropriate HTTP status codes (e.g., `OrderNotFoundException` -> 404).
- **Audit**: Every `PATCH` request must trigger a `HistorialEstadoPedido` entry via the service layer.
