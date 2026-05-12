# PROPOSAL: Orders API Formalization (Change #20)

## Intent
Formalize the Orders API endpoints to strictly adhere to the business rules defined in `Historias_de_usuario.txt`, specifically regarding the Finite State Machine (FSM), Role-Based Access Control (RBAC), and Audit Trail requirements.

## Problem
The current implementation of order routes in `backend/orders/routes.py` lacks:
1. **State Transition Validation**: It allows manual transitions that should be automatic (e.g., PENDIENTE -> CONFIRMADO).
2. **State-Dependent Permissions**: It doesn't restrict cancellation based on the order's current state (e.g., only Admin can cancel if `EN_PREPARACION`).
3. **Audit Metadata**: It doesn't capture reasons for state changes (cancellation/updates) to populate the `HistorialEstadoPedido`.
4. **Role Granularity**: It doesn't properly distinguish between `Role.PEDIDOS` (Gestor de Pedidos) and `Role.ADMIN` for administrative listing and detail views.

## Proposed Changes
1. **Endpoint Refactoring**:
   - `POST /orders`: Finalize creation logic with proper DTOs.
   - `GET /orders`: List user orders (paginated).
   - `GET /orders/{id}`: Detailed view with snapshots and history.
   - `PATCH /orders/{id}/cancel`: Formal cancellation endpoint requiring a "reason" and enforcing `RN-FS08`.
   - `PATCH /orders/{id}/status`: Administrative endpoint for Gestores/Admins to advance state (CONFIRMADO -> EN_PREPARACION -> ...).
2. **FSM Enforcement**: Integrate the `OrderService` transitions to prevent illegal jumps or manual overrides of the payment flow.
3. **RBAC Integration**: Ensure `Role.PEDIDOS` has access to the administrative dashboard view but not to user-private data unless specified.
4. **Correlation Propagation**: Ensure all endpoints correctly propagate the `x-correlation-id` to the service and monitoring layers.

## Success Criteria
- [ ] `POST /orders` creates an order in `PENDIENTE` state and returns 201.
- [ ] `PATCH /orders/{id}/cancel` correctly validates state and role (RN-FS08).
- [ ] Manual transitions to `CONFIRMADO` via API are blocked (RN-FS02).
- [ ] All state changes generate a record in `HistorialEstadoPedido`.
- [ ] Admin/Gestor listing (`GET /orders`) includes pagination and state filters (US-051).
