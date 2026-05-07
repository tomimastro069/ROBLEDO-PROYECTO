## Why

Currently, the backend throws unformatted errors or relies on FastAPI's default handlers (like `RequestValidationError`), leading to inconsistent API responses. To provide a predictable, uniform contract for the frontend, we need to implement a global exception handling architecture that strictly adheres to RFC 7807 (Problem Details for HTTP APIs).

## What Changes

- Create a base `DomainException` class for business logic errors.
- Implement global exception handlers in FastAPI for `DomainException` and `RequestValidationError`.
- **BREAKING**: All API errors, including Pydantic validation errors, will now return a JSON response formatted according to RFC 7807 (`type`, `title`, `status`, `detail`, `instance`, and optionally `invalid_params`).
- Connect these custom handlers to the FastAPI application instance in `main.py`.

## Capabilities

### New Capabilities
- `error-handling`: Standardizes all API error responses to follow the RFC 7807 specification, ensuring a consistent contract between backend and frontend.

### Modified Capabilities
- None.

## Impact

- **API Contract**: Frontend applications will need to expect RFC 7807 formatted JSON on any 4xx or 5xx response.
- **Service Layer**: Business logic will throw `DomainException` (or subclasses) instead of returning HTTP-specific tuples or raising `HTTPException`.
- **FastAPI Core**: Overrides the default `RequestValidationError` handler.