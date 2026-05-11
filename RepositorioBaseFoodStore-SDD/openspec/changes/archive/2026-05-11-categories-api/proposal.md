# Proposal: Categories API

## Intent

Expose the hierarchical categories business logic (`categories-service`) via REST API endpoints, providing a complete CRUD interface (GET, POST, PUT, DELETE) for category management. This unblocks the `products-service` which depends on having callable category endpoints.

## Scope

### In Scope
- Creation of `backend/categories/router.py` defining REST endpoints for:
  - `GET /categories` (list all, with optional hierarchy filtering)
  - `GET /categories/{id}` (get single category with details)
  - `POST /categories` (create new category)
  - `PUT /categories/{id}` (update category)
  - `DELETE /categories/{id}` (soft delete category)
- Injection of `CategoriesService` into the new router using FastAPI's `Depends`.
- Request/response schemas for category operations (Create, Update, Response payloads).
- RBAC enforcement: Only Admin and Stock Manager roles can create/update/delete categories.

### Out of Scope
- Frontend UI for category management (handled in later changes).
- Category hierarchy visualization (backend provides data; frontend handles UI).
- Bulk import/export of categories.

## Approach

Use **Feature-First Router Pattern**:
Create a cohesive `router.py` inside the `backend/categories/` feature slice. The router will depend on `get_categories_service` and delegate business logic to the `CategoriesService`. Schemas and response models will be co-located in `backend/categories/schemas.py`. The new router will be mounted in `backend/main.py` at the `/categories` path.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `backend/categories/router.py` | New | Dedicated API router for categories endpoints |
| `backend/categories/schemas.py` | New | Request/response schemas for category operations |
| `backend/main.py` | Modified | Register new categories router at `/categories` prefix |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Circular dependency if products-api imports categories | Low | Keep layers clean: Router → Service → Repository. Products service calls categories service, not router. |
| RBAC enforcement gaps | Medium | Use existing `get_current_user` dependency to validate roles before allowing write operations. |
| N+1 queries on hierarchical list | Medium | Ensure CategoriesService uses JOIN queries for nested categories; test with db monitoring. |

## Rollback Plan

Delete `backend/categories/router.py` and `backend/categories/schemas.py`, remove the router registration from `backend/main.py`.

## Dependencies

- `categories-service` (Completed in Change 13).
- `backend-core-setup` (JWT, CORS, error handling already in place).

## Success Criteria

- [ ] All CRUD endpoints work and return correct HTTP status codes (201, 200, 204, 400, 401, 403, 404).
- [ ] RBAC restrictions enforce: only Admin/Stock Manager can create/update/delete.
- [ ] GET endpoints work for public (all users) and authenticated (current user info) scenarios.
- [ ] Hierarchical structure is preserved (parent_id relationships maintained).
- [ ] `/docs` Swagger UI reflects all endpoints with proper authorization badges.
