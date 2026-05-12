## Why

As part of the Food Store application, users need to assemble their order and validate it against current inventory and pricing. We have decided to implement a "Stateless Cart" (Option A), where the frontend entirely manages the cart state and the backend only validates it during checkout. This approach minimizes backend state management overhead, reduces database load, and provides a faster, offline-tolerant experience for users compiling their orders, while still ensuring consistency at checkout.

## What Changes

- Implement a backend `CartValidationService` that cross-references a client-provided cart payload with current product availability and prices.
- Add an endpoint (e.g., `POST /api/cart/validate`) for upfront cart validation, or integrate validation strictly into the checkout/order creation process.
- Implement a persistent Zustand store (`cartStore`) on the frontend to manage cart items (add, remove, change quantity, calculate subtotals).
- Ensure the checkout flow uses the validation service to prevent overselling or price mismatches.

## Capabilities

### New Capabilities
- `cart-validation`: Backend logic to validate cart item prices, stock availability, and consistency across the catalog.
- `cart-frontend`: Client-side management of the shopping cart using Zustand, handling persistence and UI interaction.

### Modified Capabilities
- `orders-service`: Order creation must integrate with or depend on cart validation to ensure items are valid before persisting the order state.

## Impact

- **Backend**: `products` module (to query real-time stock/price), `orders` module (to consume validation), new `cart` module (for validation schemas/logic).
- **Frontend**: New global store for cart state, and updates to the checkout flow components.
- **Database**: No new tables are required for the cart itself, as it remains completely stateless on the backend.