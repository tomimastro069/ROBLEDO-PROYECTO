## Context

FastAPI natively handles validation errors via `RequestValidationError` and provides `HTTPException` for manual error raising. However, throwing `HTTPException` inside the Service layer violates clean architecture principles, as the business layer should not be coupled to HTTP concepts. Additionally, the default JSON structures returned by FastAPI vary depending on the error source. To unify the API contract for the frontend (which uses Axios and Zustand), we will implement the RFC 7807 specification for all errors.

## Goals / Non-Goals

**Goals:**
- Implement an RFC 7807 compliant error structure across the backend.
- Isolate the Service layer from HTTP details by providing a `DomainException` base class.
- Capture and format Pydantic validation errors into the RFC 7807 structure, exposing an `invalid_params` array.

**Non-Goals:**
- Refactoring existing business logic (there isn't much yet, as we are in step 8).
- Handling 500 Internal Server Errors with detailed stack traces in production (these should return a generic RFC 7807 500 error to prevent information leakage).

## Decisions

1. **Centralized Exception Module:**
   - **Decision**: Create `app/core/exceptions.py` containing both the exception classes and the FastAPI exception handlers.
   - **Rationale**: Keeps all error-related configuration in one place.

2. **DomainException Base Class:**
   - **Decision**: Create a `DomainException(Exception)` class holding `title`, `detail`, `status_code`, and `error_type`. Subclasses like `NotFoundException` will pre-fill these fields.
   - **Rationale**: Services can simply `raise NotFoundException("User not found")` without knowing that it translates to an HTTP 404.

3. **Validation Error Interception:**
   - **Decision**: Override FastAPI's default `RequestValidationError` handler. We will map Pydantic's `exc.errors()` into a custom `invalid_params` list within the RFC 7807 JSON response.
   - **Rationale**: Ensures the frontend always receives the same root keys (`type`, `title`, `status`, `detail`, `instance`), making generic error handling in Axios interceptors trivial.

## Risks / Trade-offs

- **Risk: Breaking FastAPI's Swagger UI documentation.** Sometimes overriding validation handlers can affect how OpenAPI describes the 422 responses.
  - **Mitigation**: We will accept the default OpenAPI schema for 422s for now, as the primary consumer is our own frontend which will be built to expect the RFC 7807 format.
- **Trade-off: Verbose exceptions.** Creating a subclass for every possible business error might lead to a large `exceptions.py` file.
  - **Mitigation**: We will stick to generic HTTP-analogous domain errors initially (NotFound, BadRequest, Unauthorized, Forbidden) and expand only if highly specific types are required.