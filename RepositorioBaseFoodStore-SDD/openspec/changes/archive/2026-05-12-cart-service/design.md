## Context

The Food Store project needs a way for users to build and validate a shopping cart before creating an order. Currently, products, categories, and an initial orders module exist, but there is no mechanism to cross-reference client-side selections with real-time backend data (prices, stock) prior to checkout. 

## Goals / Non-Goals

**Goals:**
- Implement a robust, stateless validation mechanism in the backend to verify cart integrity (e.g. price mismatches, out-of-stock items) at the moment of checkout or explicitly when requested.
- Provide a responsive client-side experience for building carts using Zustand for state management.
- Ensure the `orders` module correctly uses the validation before persisting an order.

**Non-Goals:**
- Server-side cart persistence (no `carts` or `cart_items` tables in the database).
- Cross-device cart synchronization (the cart lives in the local device storage).
- Expiring carts via background jobs (since the backend doesn't store them).

## Decisions

### 1. Stateless Cart Architecture
**Decision**: The backend will not store the cart state. 
**Rationale**: (Option A). This avoids unnecessary database writes for abandoned carts. It keeps the architecture simpler and relies on the client to hold the "draft" state until the user is ready to pay.
**Alternatives considered**: Server-side carts (creates unnecessary CRUD overhead and garbage collection needs) or "Draft Orders" (pollutes the orders table with unfinished carts).

### 2. Validation Delegation
**Decision**: Create a `CartValidationService` that takes a `CartDTO` and returns a boolean or throws a `CartValidationError` if prices/stock do not match the database.
**Rationale**: Decouples the order creation logic from the heavy lifting of querying multiple product variants, stock levels, and ensuring price consistency.

### 3. Frontend State Management
**Decision**: Use Zustand with `persist` middleware (targeting `localStorage`).
**Rationale**: Simple, lightweight, and ensures the user doesn't lose their selected food items if they accidentally refresh the page.

## Risks / Trade-offs

- **Risk: Price mismatch at checkout** 
  - *Trade-off*: Because the cart is stateless, a product's price might change while it's in the user's local storage.
  - *Mitigation*: The backend will strictly validate the provided total vs real-time database prices. If there is a mismatch, a specific error code will be returned so the frontend can update its state and warn the user.
- **Risk: Out of stock at checkout**
  - *Mitigation*: Same as above, validate inventory levels atomically before order creation.