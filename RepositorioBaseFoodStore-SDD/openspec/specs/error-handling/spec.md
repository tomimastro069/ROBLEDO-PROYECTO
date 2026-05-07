## ADDED Requirements

### Requirement: RFC 7807 Domain Exceptions
The system MUST provide a base `DomainException` class that encapsulates business errors, and the API MUST format these exceptions as RFC 7807 JSON objects when returned to the client.

#### Scenario: Service throws NotFoundException
- **WHEN** a service layer raises a `NotFoundException` (a subclass of `DomainException`)
- **THEN** the API returns an HTTP 404 response with a JSON body containing `type`, `title`, `status`, `detail`, and `instance` fields matching the RFC 7807 specification.

### Requirement: Pydantic Validation Errors to RFC 7807
The system MUST intercept FastAPI's default `RequestValidationError` and format it according to RFC 7807, including an `invalid_params` array that details the specific validation failures.

#### Scenario: Malformed request payload
- **WHEN** a client sends a JSON payload missing required fields
- **THEN** the API returns an HTTP 422 response with a JSON body containing the standard RFC 7807 fields plus an `invalid_params` array containing `field` and `reason` for each missing property.
