# Design Document for Orders Service

## Introduction
The `orders-service` is responsible for managing the lifecycle of orders in the system, from creation to completion, ensuring data consistency, processing business validations, and notifying other systems of changes.

---

## Technical Approach

We aim to implement the `orders-service` using a modular, event-driven approach:

1. **Services**:
   - **Order Management**: Handles CRUD operations for orders.
   - **Validation Service**: Encapsulates rules and business policies.
   - **Notification Service**: Publishes events such as order updates and completion.
   - **State Machine**: Ensures orders transition correctly between states.

2. **Data Persistence**:
   - PostgreSQL with SQLModel stores order records and audits.

3. **Communication**:
   - Publish/Subscribe mechanism using an established message broker (RabbitMQ).

---

## Modules and Services

### Order API
RESTful endpoint for interaction with the orders system.
   
### Validation Service
Encodes domain rules such as "An order cannot proceed before required stock validation."
   
### State Service
Implements order lifecycle logic, ensuring proper state transitions.

---

## Data Flow
- Orders created by users trigger validation checks.
- Successfully validated orders update inventory and proceed to payment.
- Finalized orders are stored persistently and trigger notification events.

---

