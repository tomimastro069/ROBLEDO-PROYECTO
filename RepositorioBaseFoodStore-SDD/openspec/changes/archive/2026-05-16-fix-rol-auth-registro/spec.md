# Specification: Default Client Role Assignment

## Requirements
1. **Mandatory Role**: Upon successful registration, the system MUST assign the role named `cliente` to the new user.
2. **Database Lookup**: The system MUST retrieve the `role_id` from the `roles` table before persisting the user record.
3. **Hard Failure**: If the `cliente` role does not exist in the database, the system MUST throw a `500 Internal Server Error` indicating a configuration failure.
4. **Atomicity**: The role lookup and user creation MUST occur within the same `Unit of Work` transaction to ensure atomicity.

## Acceptance Criteria
- A newly registered user must have a valid `role_id` in the database.
- The JWT token generated during login must reflect the role persisted in the database, without relying on hardcoded logic.
