# Proposal: Fix User Role Assignment during Registration

## Why
Currently, new users registered via `/auth/register` are not assigned a role in the database (`role_id` remains `NULL`). This creates a critical data inconsistency where:
- The backend relies on a hardcoded "cliente" fallback in the JWT token logic during login.
- Database queries, admin filters, and business logic that check the `User.role` relationship directly from the DB fail or return incorrect results.
- Administrative visibility of new users is impaired.

## What Changes
- **Database Consistency**: Modify `AuthService.register` to perform a lookup for the `cliente` role in the database using the Unit of Work.
- **Architectural Cleanup**: Remove legacy hardcoded fallbacks in `AuthService.login` and `AuthService.refresh`, ensuring the token reflects the actual database state.
- **Improved Error Handling**: Implement a guard clause that ensures the system fails fast if the mandatory `cliente` role is missing from the database configuration.

## Impact
- **Data Integrity**: Every user will have a valid `role_id` linked to the `roles` table upon creation.
- **Backend Reliability**: Prevents `AttributeError` (NoneType) when accessing `user.role` in other services.
- **Admin Transparency**: New users will correctly appear with the "cliente" label in the administration dashboard.
