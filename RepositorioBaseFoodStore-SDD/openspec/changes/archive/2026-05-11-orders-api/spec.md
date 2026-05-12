# DELTA SPEC: Orders API (Change #20)

## Overview
This specification defines the external API contract for order management, exposing the capabilities of the `OrderService` while enforcing security, FSM rules, and traceability.

## Requirements Mapping
- **R1: Create Order**: `POST /orders` (US-035)
- **R2: List Own Orders**: `GET /orders` (US-049)
- **R3: View Order Detail**: `GET /orders/{id}` (US-050)
- **R4: Cancel Order**: `PATCH /orders/{id}/cancel` (US-043)
- **R5: Administrative List**: `GET /admin/orders` (US-051)
- **R6: Administrative Update**: `PATCH /admin/orders/{id}/status` (US-040, US-041, US-042)

## API Contract

### 1. Create Order
- **Endpoint**: `POST /api/v1/orders`
- **Auth**: `Role.CLIENT`
- **Request Body**:
  ```json
  {
    "items": [
      { "product_id": 1, "quantity": 2, "exclusions": [5, 10] }
    ],
    "shipping_address": { "id": 1 }
  }
  ```
- **Responses**:
  - `201 Created`: Returns `OrderResponse`.
  - `400 Bad Request`: Validation error or insufficient stock.
  - `409 Conflict`: Business rule violation.

### 2. List Orders (Customer)
- **Endpoint**: `GET /api/v1/orders`
- **Auth**: `Role.CLIENT`
- **Query Params**: `skip`, `limit`, `status`
- **Response**: `PaginatedResponse[OrderResponse]`

### 3. List Orders (Admin/Gestor)
- **Endpoint**: `GET /api/v1/admin/orders`
- **Auth**: `Role.ADMIN`, `Role.PEDIDOS`
- **Query Params**: `skip`, `limit`, `status`, `user_id`, `from_date`, `to_date`
- **Response**: `PaginatedResponse[OrderAdminResponse]`

### 4. Cancel Order
- **Endpoint**: `PATCH /api/v1/orders/{id}/cancel`
- **Auth**: `Role.CLIENT` (own), `Role.ADMIN`, `Role.PEDIDOS`
- **Request Body**:
  ```json
  { "reason": "User changed mind" }
  ```
- **FSM Constraint**: Only allowed if current state is `PENDIENTE` (Client) or `CONFIRMADO` (Gestor/Admin).

## Error Handling (RFC 7807)
All endpoints must return standard problem details for:
- `order_not_found`: 404
- `invalid_state_transition`: 400
- `insufficient_stock`: 400
- `unauthorized_access`: 403
