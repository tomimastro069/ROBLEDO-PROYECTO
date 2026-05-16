# Design: Role Implementation in AuthService

## Architecture
The implementation utilizes the `RoleRepository` injected via `AppUnitOfWork` to retrieve the `Role` entity by name. This follows the existing repository pattern and ensures the service layer remains decoupled from raw SQL queries.

## Code Implementation
- **Imports**: Include `from auth.roles import Role` to utilize the standardized Role Enum.
- **Registration Logic**:
    - Invoke `uow.roles.get_by_name(Role.CLIENTE.value)`.
    - Pass the retrieved `id` to the `User` model constructor.
- **Refactoring**: 
    - Update `login` and `refresh` methods to use the role name directly from the database object (`user.role.name`).
    - Maintain a safety fallback to `Role.CLIENTE.value` only as a secondary guard for legacy data compatibility.

## Sequence Diagram
1. Frontend submits registration data to `/register`.
2. `AuthService` opens a transaction via `UoW`.
3. `UoW` fetches the `cliente` Role object from the DB.
4. `UoW` instantiates a new `User` with the provided `role_id`.
5. Transaction is committed.
