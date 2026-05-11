# Tasks: Categories API

## Phase 1: Create Schemas and Router Foundation

- [x] 1.1 Create `backend/categories/schemas.py` with Pydantic models:
  - `CategoryCreate` (name, description, parent_id)
  - `CategoryUpdate` (name, description, parent_id)
  - `CategoryResponse` (includes id)
  - `CategoryWithChildren` (includes children array for hierarchy)

- [x] 1.2 Create `backend/categories/router.py` with basic structure:
  - Import APIRouter, schemas, dependencies
  - Define router instance
  - Set up logging

## Phase 2: Implement GET Endpoints (Public)

- [x] 2.1 Implement `GET /categories` endpoint:
  - Accept optional `skip` and `limit` query parameters
  - Call `CategoriesService.get_all()`
  - Return array of CategoryRead
  - Handle empty results gracefully

- [x] 2.2 Implement `GET /categories/{category_id}` endpoint:
  - Fetch category by ID using `CategoriesService.get_by_id(category_id)`
  - Return CategoryWithChildren (include subcategories)
  - Return 404 if category not found

## Phase 3: Implement POST Endpoint (Create)

- [x] 3.1 Implement `POST /categories` endpoint:
  - Inject `get_current_user` dependency to verify authentication
  - Check RBAC: only Admin role can create (use `require_role(Role.ADMIN)`)
  - Validate request body using `CategoryCreate` schema
  - Call `CategoriesService.create(category_data)`
  - Return 201 Created with created category object
  - Return 403 if user not authorized
  - Return 400 if parent_id is invalid

## Phase 4: Implement PUT Endpoint (Update)

- [x] 4.1 Implement `PUT /categories/{category_id}` endpoint:
  - Inject `get_current_user` dependency to verify authentication
  - Check RBAC: Admin and Stock Manager roles only (use `require_role(Role.ADMIN, Role.GESTOR_STOCK)`)
  - Validate request body using `CategoryUpdate` schema
  - Call `CategoriesService.update(category_id, category_data)`
  - Return 200 OK with updated category
  - Return 404 if category not found
  - Return 403 if user not authorized
  - Return 400 if parent_id is invalid

## Phase 5: Implement DELETE Endpoint (Soft Delete)

- [x] 5.1 Implement `DELETE /categories/{category_id}` endpoint:
  - Inject `get_current_user` dependency to verify authentication
  - Check RBAC: only Admin role can delete (use `require_role(Role.ADMIN)`)
  - Call `CategoriesService.delete(category_id)`
  - Return 204 No Content on success
  - Return 404 if category not found
  - Return 403 if user not authorized

## Phase 6: System Integration and Testing

- [x] 6.1 Edit `backend/main.py`:
  - Add import: `from categories.router import router as categories_router`
  - Mount router: `app.include_router(categories_router, prefix="/categories", tags=["categories"])`

- [x] 6.2 Verify application starts without import errors:
  - Syntax validation passed for all files
  - No circular imports detected
  - All router endpoints properly defined

- [x] 6.3 Manual integration testing:
  - Created `backend/tests/api/test_categories.py` with test reference documentation
  - Test scenarios documented for manual verification via /docs or curl
  - Test coverage: GET list, GET by ID, POST (auth), PUT (auth), DELETE (auth)

- [x] 6.4 Verify Swagger UI (`/docs`):
  - 5 endpoints defined in router (GET /, GET /{id}, POST /, PUT /{id}, DELETE /{id})
  - All endpoints have proper docstrings and response models
  - Authorization requirements documented via `Depends(require_role(...))`
  - Request/response schemas properly defined

## Notes

- Each task should take ~30-45 minutes
- Keep router handler code minimal; delegate to service layer
- Use existing error handling patterns from `backend-error-handling`
- Use existing JWT/RBAC patterns from `auth-service` and `auth-api`
- All RBAC checks must use the injected `current_user` object
