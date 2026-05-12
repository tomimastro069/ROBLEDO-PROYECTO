## ADDED Requirements

### Requirement: Client-Side Cart State
The frontend system SHALL maintain the cart state using a local store (Zustand) and persist it across browser sessions using local storage.

#### Scenario: Adding an item to the cart
- **WHEN** the user adds a product to the cart
- **THEN** the cart store MUST increase the quantity if the product is already in the cart
- **THEN** the cart store MUST append the product if it is not in the cart
- **THEN** the cart store MUST persist the updated state to local storage

#### Scenario: Subtotal calculation
- **WHEN** the cart state changes (items added, removed, or quantities updated)
- **THEN** the cart store MUST dynamically calculate and update the total price based on the current items and their quantities
