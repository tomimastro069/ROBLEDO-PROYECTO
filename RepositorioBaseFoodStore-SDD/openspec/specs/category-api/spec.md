# Specification: Category API

**Capability**: REST API for hierarchical category management  
**Status**: IMPLEMENTED (Change #14, archived 2026-05-11)  
**Implemented By**: categories-api router + CategoriesService

## Overview

The Category API exposes the business logic from `CategoriesService` via REST HTTP endpoints, providing complete CRUD operations for managing hierarchical categories. Categories are public-readable (by all roles) but write operations (create, update, delete) are restricted to Admin and Stock Manager roles.

## Requirements

### R1: Category Listing
**What**: Retrieve all active categories with optional pagination  
**Who**: All users (public endpoint)  
**URL**: `GET /categories`  
**Query Parameters**:
- `skip` (optional, default=0): Offset for pagination
- `limit` (optional, default=100): Max items to return

**Response (200 OK)**:
```json
[
  {
    "id": 1,
    "name": "Bakery",
    "description": "Baked goods",
    "parent_id": null
  },
  {
    "id": 2,
    "name": "Bread",
    "description": "Bread products",
    "parent_id": 1
  }
]
```

**Response (400 Bad Request)**: Invalid query parameters

### R2: Category Details with Hierarchy
**What**: Retrieve single category with all child categories nested  
**Who**: All users (public endpoint)  
**URL**: `GET /categories/{id}`

**Response (200 OK)**:
```json
{
  "id": 1,
  "name": "Bakery",
  "description": "Baked goods",
  "parent_id": null,
  "subcategories": [
    {
      "id": 2,
      "name": "Bread",
      "description": "Bread products",
      "parent_id": 1,
      "subcategories": []
    }
  ]
}
```

**Response (404 Not Found)**: Category does not exist

### R3: Create Category
**What**: Create a new category with optional parent (for hierarchies)  
**Who**: Admin, Stock Manager (RBAC enforced)  
**URL**: `POST /categories`  
**Headers**: `Authorization: Bearer <JWT_TOKEN>`

**Request**:
```json
{
  "name": "Desserts",
  "description": "Sweet desserts",
  "parent_id": null
}
```

**Response (201 Created)**:
```json
{
  "id": 3,
  "name": "Desserts",
  "description": "Sweet desserts",
  "parent_id": null
}
```

**Response (400 Bad Request)**:
- `"Category name already exists at this level"`
- `"Parent category with id={id} not found"`
- `"Invalid request body"`

**Response (401 Unauthorized)**: Missing or invalid JWT

**Response (403 Forbidden)**: User role is not Admin or Stock Manager

### R4: Update Category
**What**: Update category name, description, and/or parent  
**Who**: Admin, Stock Manager (RBAC enforced)  
**URL**: `PUT /categories/{id}`  
**Headers**: `Authorization: Bearer <JWT_TOKEN>`

**Request**:
```json
{
  "name": "Desserts Updated",
  "description": "All sweet treats",
  "parent_id": null
}
```

**Response (200 OK)**:
```json
{
  "id": 3,
  "name": "Desserts Updated",
  "description": "All sweet treats",
  "parent_id": null
}
```

**Response (400 Bad Request)**:
- `"Category name already exists at this level"`
- `"A category cannot be its own parent"`
- `"Parent category with id={id} not found"`

**Response (404 Not Found)**: Category does not exist

**Response (403 Forbidden)**: User role is not Admin or Stock Manager

### R5: Delete Category (Soft Delete)
**What**: Soft-delete a category (mark as deleted, preserve audit trail)  
**Who**: Admin (RBAC enforced)  
**URL**: `DELETE /categories/{id}`  
**Headers**: `Authorization: Bearer <JWT_TOKEN>`

**Response (204 No Content)**: Category deleted successfully

**Response (404 Not Found)**: Category does not exist

**Response (409 Conflict)**:
- `"Cannot delete category with active subcategories. Delete subcategories first."`

**Response (403 Forbidden)**: User role is not Admin

## Behavioral Constraints

### Soft Delete Behavior
- When a category is deleted, it is marked with a `deleted_at` timestamp
- All category queries (list, details) exclude soft-deleted records
- Soft-deleted categories are preserved in the database for audit/recovery purposes
- Cascade behavior: Products referencing deleted categories still exist; category queries will not return the deleted category

### Hierarchical Integrity
- A category cannot be its own parent (no self-reference)
- A category cannot have both a parent and children in a circular chain
- Parent category must exist before assignment
- Deleting a category with active children is forbidden

### RBAC Matrix
| Endpoint | Method | Public | Client | Stock Manager | Admin |
|----------|--------|--------|--------|---------------|-------|
| /categories | GET | ✅ | ✅ | ✅ | ✅ |
| /categories/{id} | GET | ✅ | ✅ | ✅ | ✅ |
| /categories | POST | ❌ | ❌ | ✅ | ✅ |
| /categories/{id} | PUT | ❌ | ❌ | ✅ | ✅ |
| /categories/{id} | DELETE | ❌ | ❌ | ❌ | ✅ |

## Data Model

```
Category (domain model in app.core.models.Category):
  - id: int (primary key)
  - name: str (required, indexed)
  - description: str (optional)
  - parent_id: int (optional, foreign key to Category.id)
  - deleted_at: datetime (optional, soft-delete audit trail)
  - Relationship: subcategories (one-to-many to self)
```

## HTTP Headers & Content Types

- **Request Content-Type**: `application/json`
- **Response Content-Type**: `application/json`
- **Authorization**: `Authorization: Bearer <JWT_TOKEN>` (for write operations)

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Human-readable error message"
}
```

Common HTTP status codes:
- `200 OK`: Successful GET or PUT
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Validation error
- `401 Unauthorized`: Missing/invalid JWT
- `403 Forbidden`: User lacks required role
- `404 Not Found`: Resource does not exist
- `409 Conflict`: Business rule violation (e.g., category with children)

## Implementation Details

### File Locations
- **Router**: `backend/categories/router.py`
- **Service**: `backend/categories/service.py` (CategoryService)
- **Repository**: `backend/app/core/repositories/category_repository.py`
- **Schemas**: `backend/categories/schemas.py`
- **Models**: `backend/app/core/models.py` (Category)
- **Tests**: `backend/tests/api/test_categories_integration.py`

### Dependencies
- FastAPI for HTTP routing
- SQLModel for ORM/Pydantic
- SQLAlchemy for database operations
- JWT for authentication
- RBAC middleware for role checking

### Testing Coverage
- 21 integration test cases
- CRUD operations (list, get, create, update, delete)
- RBAC enforcement for all roles
- Business rule validation (hierarchy, uniqueness, no children on delete)
- Soft-delete verification
- Error handling (400, 403, 404, 409)

## Pagination

List endpoint supports cursor-based pagination via `skip` and `limit` query parameters:
- `skip=0&limit=50`: Return first 50 categories
- `skip=50&limit=50`: Return next 50 categories
- Default: `skip=0, limit=100`

## Related Capabilities

- **Depends on**: Authentication API, Role-based Access Control
- **Depended on by**: Product API (categories referenced in products), Cart Service (categories for browsing)
- **Complements**: Categories Service (Change #13, business logic layer)

## Versioning & Deprecation

Current API version: **v1** (implicit, not in URL path)  
No deprecated endpoints at this time.

## Notes & Future Enhancements

1. **Full-Text Search**: Add `GET /categories/search?q=...` for keyword search
2. **Bulk Operations**: Add `POST /categories/bulk-import` for CSV import
3. **Category Images**: Add image upload for visual category representation
4. **Analytics**: Track category popularity via product/order counts
5. **Advanced Hierarchy**: Support multiple parent categories (graph instead of tree)
