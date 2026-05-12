# Orders Service Specifications

## Functional Requirements

### Core Functionalities
1. **Order Creation**:
   - Endpoint for creating a new order.
   - Input: Order details (user ID, product details, quantities, special instructions, etc.).
   - Output: Order ID, creation timestamp, calculated total, status (e.g., drafted, submitted).

2. **Order Retrieval**:
   - Retrieve an order by its ID.
   - Retrieve orders by user ID with optional pagination and filters (e.g., by date, status).

3. **Order Status Update**:
   - Update order statuses: **Draft**, **Submitted**, **Processing**, **Completed**, **Cancelled**.
   - Event-driven communication with other services on specific status changes (e.g., notify payment service on "Submitted" status).

4. **Order Cancellation**:
   - Allow users to cancel orders before transitioning to "Processing."
   - Automatically notify associated services (inventory adjustment, payment refund).

5. **Order Validation**:
   - Validate product availability (via inventory service).
   - Validate prices (via catalog service).
   - Validate payment methods (via payment gateway).

6. **Notifications**:
   - Notify users of order status changes (email or push notifications).
   - Allow consumers to subscribe to WebSocket channels for real-time updates.

### Integration Requirements
1. **Communication with Inventory Service**:
   - Verify stock levels before confirming orders.
   - Deduct stock when the order is "Submitted".
   - Revert stock on "Cancelled" or "Failed" orders.

2. **Communication with Payment Service**:
   - Confirm payment on "Processing" orders.
   - Refund payment on "Cancelled" or failed orders.

3. **Communication with Delivery Service**:
   - Automatically schedule delivery for "Completed" orders.

4. **Event Bus Integration**:
   - Publish order events for status changes (`OrderCreated`, `OrderUpdated`, `OrderCancelled`).

### Administrative Features
1. **Order Reports**:
   - Administrative access to order analytics (total revenue, most ordered products, etc.).
   - Export functionality for reports (CSV, PDF).

2. **Order Management**:
   - Modify orders manually (by Admin) in case of discrepancies or issues.

---

## Non-Functional Requirements

### Scalability
- Support 10,000 concurrent order submissions.
- Handle spikes during promotions (up to 5x the regular traffic).

### Performance
- **Order creation** latency: Max 200ms under normal load.
- **Order retrieval** latency: Max 100ms under normal load.

### Reliability
- Ensure message delivery between services for all critical events (at-least-once delivery).
- Orders Service must maintain 99.95% uptime.

### Security
- Ensure user authentication with JWT tokens.
- Role-based access control:
  - Users: Manage their orders only.
  - Admins: Access all orders.
- Secure sensitive data (e.g., payment confirmation, user info) via encryption.

### Data Integrity
- Preserve integrity between services through distributed transaction mechanisms or compensating actions.

### Observability
- Logs for all API requests, responses, and events:
  - Use correlation IDs for tracing requests.
- Metrics for monitoring (order events processed per second, latencies).

### Compatibility
- Platform-independent and cloud-agnostic APIs using OpenAPI 3.0 specifications.
- Support for REST and gRPC communication.

---

## Use Cases & Scenarios

### 1. Order Creation
#### Scenario 1.1: User places an order.
**Steps**:
1. User sends `POST /orders` with details.
2. Orders Service validates request.
3. Orders Service confirms product availability via Inventory Service.
4. Orders Service calculates total cost.
5. Service responds with `201 Created` and the order details.
6. Publish event `OrderCreated`.

**Constraints**:
- Ensure validation occurs within 100ms.

---

### 2. Order Status Update
#### Scenario 2.1: User updates order status to "Submitted".
**Steps**:
1. User sends `PATCH /orders/{id}` request updating status.
2. Orders Service confirms:
   - Inventory stock lock.
   - Authorizes payment method (Payment Service).
3. Service updates order record.
4. Publish event `OrderSubmitted` to Event Bus.

---

### 3. Order Cancellation
#### Scenario 3.1: User cancels an order.
**Steps**:
1. User sends `DELETE /orders/{id}` before "Processing" status.
2. Orders Service checks the order’s current status.
3. If eligible:
   - Reverts inventory stock.
   - Requests payment refund.
4. Publish event `OrderCancelled`.

#### Constraints:
- Cancellation only allowed before "Processing".

---

### 4. Error Handling
#### Scenario 4.1: Inventory Service reports insufficient stock.
**Steps**:
1. Orders Service receives stock validation failure.
2. Service responds with `409 Conflict` status, including error details.

---

## Constraints

1. **Database Constraints**:
   - Orders must be consistent in the database with associated inventory and payment records.
   - Index for quick retrievals on `user_id`, `status`, `created_at`.

2. **Message Queue Reliability**:
   - Use idempotency tokens to handle duplicate message delivery.

3. **Timeouts**:
   - Service-to-service calls must timeout after 3 seconds, with retries capped at 2 attempts.

4. **Event Schema**:
   - Uniform schema for all events (`OrderCreated`, `OrderSubmitted` with consistent fields across services).

---

