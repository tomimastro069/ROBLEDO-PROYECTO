# DELTA SPEC: Product Ingredients Integration (Change #28)

## Overview
This specification defines the functional contract for mapping, querying, and updating food ingredients for any product, preserving dietary compliance guidelines and preventing interface distortion in administrative modules.

## Requirements Mapping
- **R1: Product Creation with Ingredients**: `POST /products` (US-026)
- **R2: Detailed Product Fetch**: `GET /products/{id}` (US-027)
- **R3: Relational Modification mapping**: `PUT/PATCH /products/{id}` (US-028)
- **R4: High-Performance Search and Selection Component**: Search Bar (US-029)
- **R5: Allergen Label Alerts**: Warning indicators (US-030)

## API Contract

### 1. Create Product
- **Endpoint**: `POST /api/v1/products`
- **Auth**: `Role.ADMIN`
- **Request Body**:
  ```json
  {
    "name": "Pizza Especial",
    "description": "Jamón, morrón y olivas",
    "price": 1500.0,
    "stock": 40,
    "category_id": 1,
    "ingredient_ids": [1, 2, 4]
  }
  ```
- **Responses**:
  - `201 Created`: Returns `ProductWithIngredients` schema.
  - `400 Bad Request`: Validation errors.

### 2. Update Product
- **Endpoint**: `PATCH /api/v1/products/{id}`
- **Auth**: `Role.ADMIN`
- **Request Body**:
  ```json
  {
    "price": 1600.0,
    "ingredient_ids": [1, 4]
  }
  ```
- **Responses**:
  - `200 OK`: Returns updated product profile.
  - `404 Not Found`: Product identifier not active in catalog.

## Error Handling
The backend service maps exception objects to standard HTTP codes:
- `product_not_found`: 404
- `invalid_ingredient_relation`: 400
- `circular_recursion_loop`: 500
