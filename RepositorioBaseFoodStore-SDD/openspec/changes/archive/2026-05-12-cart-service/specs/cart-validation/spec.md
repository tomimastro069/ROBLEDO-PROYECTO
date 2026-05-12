## ADDED Requirements

### Requirement: Stateless Cart Validation
The system SHALL validate cart items (price, stock, consistency) synchronously during the validation process without storing the cart in the database.

#### Scenario: Valid cart
- **WHEN** a client submits a cart validation request containing valid product IDs, quantities within available stock limits, and prices matching the database
- **THEN** the system MUST return a success response
- **THEN** the system MUST NOT create any new records in the database

#### Scenario: Price mismatch
- **WHEN** a client submits a cart validation request where an item's price does not match the current database price
- **THEN** the system MUST return an error indicating a price mismatch
- **THEN** the response MUST include the current correct prices

#### Scenario: Out of stock
- **WHEN** a client submits a cart validation request where an item's requested quantity exceeds available stock
- **THEN** the system MUST return an error indicating insufficient stock
- **THEN** the response MUST specify which product lacks stock