## Why

The current cart frontend setup has an architectural violation under Feature-Sliced Design (FSD). The `CartDrawer.tsx` is located in `entities/cart`, but it aggregates multiple UI components and business logic, which conceptually belongs in `widgets/cart`. Additionally, the specific user interactions for adding items, removing items, and changing quantities are missing and need to be implemented as distinct `features` to keep the codebase modular, reusable, and strictly aligned with FSD principles before we integrate with the backend cart service.

## What Changes

- **Move** `CartDrawer.tsx` from `entities/cart/ui` to `widgets/cart/ui`.
- **Create** `AddToCart` feature component (button with logic to add a product to the cart).
- **Create** `RemoveFromCart` feature component (trash icon/button to remove an item).
- **Create** `ChangeQuantity` feature component (+/- controls for item quantity).
- **Create** `CartButton` widget (Header icon with an item count badge).
- **Refactor** `entities/cart` to solely contain the Zustand store (`model/cartStore.ts`) and pure UI components (e.g., `CartItem.tsx` without business logic).

## Capabilities

### New Capabilities
- `cart-management-ui`: Frontend user interface capabilities for managing the shopping cart (adding, removing, updating quantities) and visualizing the cart state via a drawer and header badge.

### Modified Capabilities
- *None*

## Impact

- **Frontend Architecture**: Enforces strict FSD by properly separating features, widgets, and entities.
- **UI/UX**: Users will have working buttons on product cards to add to the cart, a header badge showing total items, and functional controls inside the cart drawer.
- **Code**: Refactors imports for `CartDrawer` across the application (likely in the main layout or providers where it is currently used).
