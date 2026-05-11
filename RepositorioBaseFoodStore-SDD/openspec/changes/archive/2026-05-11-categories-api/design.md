# Design: Categories API

## Technical Approach

Create a dedicated `backend/categories/router.py` to expose the `CategoriesService` logic over HTTP. By using FastAPI's dependency injection (`Depends`), the router handlers will request an instance of `CategoriesService` and execute business logic, mapping Pydantic schemas correctly. The router will enforce RBAC using the existing `get_current_user` dependency.

## Architecture Decisions

### Decision: Endpoint Structure

**Choice**: Use standard REST conventions with resource-based URLs (`/categories`, `/categories/{id}`)
**Alternatives considered**: GraphQL or RPC-style endpoints.
**Rationale**: REST is simpler, more cacheable, and aligns with existing auth-api patterns. It's idiomatic for FastAPI and easy for frontend to consume.

### Decision: Public Read vs Authenticated Write

**Choice**: 
- `GET /categories` and `GET /categories/{id}` → public (no auth required, visible to all roles)
- `POST`, `PUT`, `DELETE` → require auth + Admin or Stock Manager role

**Alternatives considered**: All endpoints require authentication.
**Rationale**: Categories are product data that customers need to browse. Writes should be restricted to staff. This aligns with the domain model where customers browse categories, but only staff manage them.

### Decision: Schema Co-location

**Choice**: Store category schemas in `backend/categories/schemas.py`
**Alternatives considered**: Global schemas in `backend/app/schemas/`
**Rationale**: Follows Feature-First pattern: categories router, service, schemas are all together. Easier to understand, modify, and test independently.

### Decision: Soft Delete vs Hard Delete

**Choice**: Soft delete (mark `deleted_at` timestamp)
**Alternatives considered**: Hard delete (remove from DB).
**Rationale**: Preserves referential integrity for products and orders that reference categories. Audit trail is maintained.

## Data Flow

```
[HTTP Request]  
       │
       ├─(GET /categories)─→ [Router] ──(get_categories_service)──→ [CategoriesService] ──→ [Repository] ──→ DB
       │
       ├─(POST /categories)─→ [Router] ──(get_current_user, RBAC check)──→ [CategoriesService] ──→ DB
       │
       └─(PUT /categories/{id})─→ [Router] ──(get_current_user, RBAC check)──→ [CategoriesService] ──→ DB
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `backend/categories/router.py` | Create | FastAPI APIRouter with CRUD endpoints |
| `backend/categories/schemas.py` | Create | Pydantic schemas for request/response payloads |
| `backend/main.py` | Modify | Import and register categories router at `/categories` prefix |

## Interfaces / Contracts

```python
# HTTP API Contracts

# GET /categories
# Query params: ?skip=0&limit=100 (optional, for pagination)
# Response 200: [ { "id": int, "name": str, "description": str, "parent_id": int|null, "created_at": str, "updated_at": str }, ... ]

# GET /categories/{id}
# Response 200: { "id": int, "name": str, "description": str, "parent_id": int|null, "children": [...], "created_at": str, "updated_at": str }
# Response 404: { "detail": "Category not found" }

# POST /categories
# Headers: Authorization: Bearer <token>
# Request: { "name": str, "description": str, "parent_id": int|null }
# Response 201: { "id": int, "name": str, "description": str, "parent_id": int|null, "created_at": str }
# Response 400: { "detail": "Invalid parent category" }
# Response 403: { "detail": "Not authorized to create categories" }

# PUT /categories/{id}
# Headers: Authorization: Bearer <token>
# Request: { "name": str, "description": str, "parent_id": int|null }
# Response 200: { "id": int, "name": str, "description": str, "parent_id": int|null, "updated_at": str }
# Response 404: { "detail": "Category not found" }
# Response 403: { "detail": "Not authorized to update categories" }

# DELETE /categories/{id}
# Headers: Authorization: Bearer <token>
# Response 204: No Content
# Response 404: { "detail": "Category not found" }
# Response 403: { "detail": "Not authorized to delete categories" }
```

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Integration | `GET /categories` | Call API, assert 200 OK and list structure |
| Integration | `GET /categories/{id}` | Call with valid ID, assert 200 OK; call with invalid ID, assert 404 |
| Integration | `POST /categories` | Call as Admin, assert 201 Created; call as Client, assert 403 Forbidden |
| Integration | `PUT /categories/{id}` | Call as Admin with valid payload, assert 200 OK |
| Integration | `DELETE /categories/{id}` | Call as Admin, assert 204 No Content; verify soft delete in DB |

## Migration / Rollout

No database migration required. Router can be mounted at any time after `categories-service` is available.

## Open Questions
- None.
