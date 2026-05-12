## Context

The current `cart-frontend` state includes a well-defined `cartStore.ts` using Zustand inside `entities/cart/model`. However, the UI components are improperly organized according to Feature-Sliced Design (FSD). `CartDrawer.tsx` is currently inside `entities`, which violates FSD principles as it orchestrates multiple behaviors and components. To build a robust and scalable cart system, we need to extract distinct user actions into `features`, assemble them into `widgets`, and leave pure state and dumb components in `entities`.

## Goals / Non-Goals

**Goals:**
- Adhere strictly to Feature-Sliced Design (FSD) for the cart module.
- Provide reusable feature components (`AddToCart`, `RemoveFromCart`, `ChangeQuantity`) that can be plugged into product lists, product detail pages, and the cart drawer.
- Create a `CartDrawer` and `CartButton` widget to orchestrate the cart experience.
- Rely on the existing Zustand `useCartStore` for state management without altering its core logic.

**Non-Goals:**
- Integration with the backend `cart-service` (this change focuses entirely on client-side UI and state).
- Checkout process or payment integration (handled in subsequent changes).
- Changing the existing `useCartStore` schema.

## Decisions

**1. FSD Mapping for Cart:**
- **Entities (`entities/cart`)**: Will hold the `cartStore.ts` (existing) and a new `CartItemUI.tsx` (pure UI component for rendering a cart row, accepting props and callbacks, no direct store hooks).
- **Features (`features/cart`)**: 
  - `AddToCart`: A button that reads from a product prop and calls `useCartStore.getState().addItem()`.
  - `RemoveFromCart`: A small button/icon that takes an `itemId` and calls `removeItem()`.
  - `ChangeQuantity`: A composite UI (minus button, quantity display, plus button) that calls `updateQuantity()`.
- **Widgets (`widgets/cart`)**: 
  - `CartDrawer`: Connects to `useCartStore` to map over items, renders `CartItemUI` injected with `RemoveFromCart` and `ChangeQuantity` features as slots/children.
  - `CartButton`: A button typically placed in the Header, hooked to `useCartStore` to display the total number of items as a badge, and toggles the `CartDrawer`.

**2. Component Composition strategy:**
- To avoid tight coupling, `entities/cart/ui/CartItemUI` will not import features directly. It will accept `actionSlot` or explicit props for the controls, allowing the `CartDrawer` widget to compose them together.

**3. Test Architecture (Mock Strategy):**
- **Unit Tests**: We will write unit tests for the new feature components (`AddToCart`, `ChangeQuantity`, `RemoveFromCart`) mocking the `useCartStore` actions to ensure they dispatch correct payloads.
- **Component Tests**: `CartDrawer` will be tested using Vitest and React Testing Library, wrapping it with an initial Zustand state to verify rendering and totals calculation.

## Risks / Trade-offs

- **Risk:** Over-engineering component slots in `CartItemUI` might make it harder to read.
  - *Mitigation:* Keep the slots simple (e.g., passing a generic `actions={...}` ReactNode prop) rather than strictly passing individual components if it becomes too verbose.
- **Risk:** FSD circular dependencies if a feature imports a widget.
  - *Mitigation:* Strict adherence to imports (app -> pages -> widgets -> features -> entities -> shared). We will use ESLint boundaries if configured, or enforce it via code review.
