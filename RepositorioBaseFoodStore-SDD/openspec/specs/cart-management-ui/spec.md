## ADDED Requirements

### Requirement: Add item to cart
The system SHALL allow users to add an item to the shopping cart, initializing the quantity at 1 or increasing it if it already exists.

#### Scenario: Add a new item
- **GIVEN** an empty cart or a cart without the selected product
- **WHEN** the user clicks the "Add to Cart" button for a product
- **THEN** the product is added to the cart store with quantity 1
- **AND** the cart total value is updated accordingly

#### Scenario: Add an existing item
- **GIVEN** a cart that already contains the selected product
- **WHEN** the user clicks the "Add to Cart" button for the same product
- **THEN** the product's quantity in the cart store is increased by 1
- **AND** the cart total value is updated accordingly

### Requirement: Remove item from cart
The system SHALL allow users to completely remove a specific item from the shopping cart.

#### Scenario: Remove item via trash button
- **GIVEN** a cart with one or more items
- **WHEN** the user clicks the remove/trash button for a specific item
- **THEN** that item is completely removed from the cart store
- **AND** the cart total value is recalculated without that item

### Requirement: Update item quantity
The system SHALL allow users to directly increment or decrement the quantity of an item in the cart.

#### Scenario: Increment item quantity
- **GIVEN** a cart with an item
- **WHEN** the user clicks the "+" control on the item's quantity selector
- **THEN** the quantity of that item increases by 1
- **AND** the cart total is updated

#### Scenario: Decrement item quantity
- **GIVEN** a cart with an item whose quantity is greater than 1
- **WHEN** the user clicks the "-" control on the item's quantity selector
- **THEN** the quantity of that item decreases by 1
- **AND** the cart total is updated

### Requirement: Cart UI Indicators
The system SHALL display the total number of items in the cart via a header badge and provide a drawer interface to manage the items.

#### Scenario: View cart badge
- **GIVEN** a user browsing the site
- **WHEN** there are items in the cart store
- **THEN** the CartButton in the header displays a badge with the total number of items
- **AND** clicking the button toggles the CartDrawer visibility
