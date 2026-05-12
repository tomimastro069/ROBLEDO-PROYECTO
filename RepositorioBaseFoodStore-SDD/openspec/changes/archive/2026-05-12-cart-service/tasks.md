## 1. Backend: Cart Validation Core

- [x] 1.1 Create `CartItemDTO` and `CartValidationRequestDTO` schemas for incoming cart data
- [x] 1.2 Implement `CartValidationService` to cross-reference cart items with real database prices and stock
- [x] 1.3 Create unit tests for `CartValidationService` covering valid cases, price mismatches, and stock shortages

## 2. Backend: API and Orders Integration

- [x] 2.1 Add `POST /api/cart/validate` endpoint for explicit frontend validation
- [x] 2.2 Update `orders/service.py` to use `CartValidationService` before confirming order creation
- [x] 2.3 Add integration tests for the updated order creation flow with validation

## 3. Frontend: Zustand State Management

- [x] 3.1 Define `CartItem` and state interfaces for the frontend store
- [x] 3.2 Implement `cartStore.ts` using Zustand with `persist` middleware for local storage
- [x] 3.3 Add store actions: `addItem`, `removeItem`, `updateQuantity`, `clearCart`, and `getTotal`

## 4. Frontend: UI and Checkout Flow

- [x] 4.1 Build `CartDrawer` or equivalent UI component to display the cart's contents and subtotal
- [x] 4.2 Connect product catalog "Add to Cart" buttons to the `cartStore`
- [x] 4.3 Integrate the `POST /api/cart/validate` call into the checkout process, handling errors visually for the user
