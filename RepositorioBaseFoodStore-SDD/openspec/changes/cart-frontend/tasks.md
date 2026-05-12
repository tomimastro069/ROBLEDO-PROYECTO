## 1. Entities and Base UI

- [x] 1.1 Extract pure UI for cart item into `frontend/src/entities/cart/ui/CartItemUI.tsx`.
- [x] 1.2 Update/Verify `frontend/src/entities/cart/model/cartStore.ts` ensuring it is strictly pure state logic.

## 2. Features Implementation

- [x] 2.1 Implement `frontend/src/features/cart/AddToCart/ui/AddToCartButton.tsx` linking to store.
- [x] 2.2 Implement `frontend/src/features/cart/RemoveFromCart/ui/RemoveButton.tsx` linking to store.
- [x] 2.3 Implement `frontend/src/features/cart/ChangeQuantity/ui/QuantityControls.tsx` linking to store.
- [x] 2.4 Add component tests (using TDD) for `AddToCartButton`, `RemoveButton`, and `QuantityControls`.

## 3. Widgets Assembly

- [x] 3.1 Move `CartDrawer.tsx` from `entities/cart` to `frontend/src/widgets/cart/ui/CartDrawer.tsx`.
- [x] 3.2 Refactor `CartDrawer.tsx` to render `CartItemUI` injected with `RemoveFromCart` and `ChangeQuantity` components.
- [x] 3.3 Create `frontend/src/widgets/cart/ui/CartButton.tsx` to toggle the drawer and show the total items badge.
- [x] 3.4 Clean up any broken imports caused by moving the `CartDrawer`.

## 4. Integration

- [ ] 4.1 Mount `CartButton` in the main header/layout of the application.
- [ ] 4.2 Verify the `CartDrawer` correctly displays globally over the layout.
- [ ] 4.3 Add `AddToCart` buttons to the product listing components (if available) to ensure full flow functionality.
