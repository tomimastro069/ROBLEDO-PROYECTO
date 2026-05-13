# Orders Service Specifications

## Functional Requirements

### Core Functionalities
1. **Order Creation**:
   - Endpoint: `POST /api/v1/orders/`.
   - Input: Order items (product ID, quantity, exclusions), shipping address ID.
   - Output: Order ID, status (PENDIENTE), calculated total (Decimal), and snapshots of the shipping address.
   - Requirement: Stock availability must be validated before creation.

2. **Order Retrieval**:
   - Retrieve an order by its ID (owner or Admin/Gestor only).
   - List personal orders with pagination.
   - List all orders for Admins/Gestores with filtering.

3. **Order Status Management (FSM)**:
   - Valid Statuses: **PENDIENTE**, **CONFIRMADO**, **EN_PREPARACION**, **EN_CAMINO**, **ENTREGADO**, **CANCELADO**.
   - Rule: Transitions must follow the formal State Machine map.
   - Rule: Transitions to **CONFIRMADO** are automatic (via payment).

4. **Order Cancellation (RN-FS08)**:
   - Client: Can cancel only if status is **PENDIENTE**.
   - Admin/Gestor: Can cancel if status is **PENDIENTE** or **CONFIRMADO**.
   - Audit: A mandatory "reason" must be provided and recorded in the history.

5. **Order Validation**:
   - Atomic stock validation and deduction.
   - Snapshotting of price and address to ensure order immutability.

### Integration Requirements
1. **Inventory Service**: Atomic stock deduction on order creation (or confirmation depending on strategy).
2. **Payment Service**: Automatic transition to **CONFIRMADO** upon successful payment webhook.
3. **Event Bus**: Publish `OrderCreated`, `OrderSubmitted`, `OrderCancelled`, and `OrderUpdated` events.

---

## Non-Functional Requirements

### Performance
- Creation latency: < 200ms.
- Financial precision: Use `Decimal` for all currency calculations.

### Security (RBAC)
- **Role.CLIENT**: Manage own orders, cancel in PENDIENTE.
- **Role.PEDIDOS / Role.ADMIN**: Full administrative access, manual state progression (except CONFIRMADO).

### Observability
- Use `x-correlation-id` in all logs and service calls.
- Audit Trail: Every state change must be recorded in `HistorialEstadoPedido`.

---

## Use Cases & Scenarios

### 1. Order Creation
1. User sends items and address.
2. Service validates stock and price snapshots.
3. Order is created in **PENDIENTE** state.

### 2. Administrative Status Update
1. Admin advances order from **CONFIRMADO** to **EN_PREPARACION**.
2. Service validates FSM transition.
3. System logs the change and notifies the user.

#### Scenario 1.2: Successful Order Creation with Validation (UPDATED)
The system SHALL validate the provided order items against the database (pricing and availability) using the CartValidationService before creating an order record.

**Steps**:
1. User sends `POST /orders` with product IDs and quantities.
2. Orders Service invokes CartValidationService to validate stock and prices.
3. Upon successful validation, Orders Service creates the order and transitions to initial state (e.g., PENDING).
4. Service responds with `201 Created` and the order details.
5. Publish event `OrderCreated`.

**Constraints**:
- Validation using CartValidationService must complete within 100ms.

#### Scenario 1.3: Order Creation fails Validation (NEW)
**Steps**:
1. User sends `POST /orders` with product IDs and quantities.
2. Orders Service invokes CartValidationService.
3. CartValidationService detects a price mismatch or insufficient stock.
4. Orders Service returns `400 Bad Request` or `409 Conflict` with validation error details.
5. The order is NOT created.

**Constraints**:
- Order creation only succeeds after CartValidationService passes all checks.

---

## ADDED Requirements (checkout-mercado-pago)

### Requirement: Integración de Pagos en la Orquestación de Pedidos
La capa de servicio de pedidos MUST proveer los métodos transaccionales para que el servicio de pagos actualice de forma atómica el estado del pedido ante confirmaciones de pasarela.

#### Scenario: Transición orquestada por Webhook de MercadoPago
- **WHEN** se invoca la confirmación de pago exitoso desde el listener de notificaciones IPN
- **THEN** la capa de servicio MUST verificar que el pedido se encuentre en estado PENDIENTE y avanzar de forma segura a CONFIRMADO dentro de los límites de la Unidad de Trabajo (UoW)
