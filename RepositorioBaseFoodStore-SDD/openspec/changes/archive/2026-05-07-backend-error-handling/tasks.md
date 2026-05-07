## 1. Domain Exception Classes

- [x] 1.1 Create `backend/app/core/exceptions.py`.
- [x] 1.2 Define the base `DomainException` class containing `title`, `detail`, `status_code`, and `error_type` attributes.
- [x] 1.3 Create common subclasses like `NotFoundException` (404), `BadRequestException` (400), and `UnauthorizedException` (401) with pre-filled status codes and standard types.

## 2. Exception Handlers

- [x] 2.1 Implement `domain_exception_handler` in `exceptions.py` to catch `DomainException` and return a `JSONResponse` matching the RFC 7807 structure.
- [x] 2.2 Implement `validation_exception_handler` in `exceptions.py` to catch FastAPI's `RequestValidationError`.
- [x] 2.3 Extract the `exc.errors()` in the validation handler to map them into an `invalid_params` array consisting of `field` and `reason`.

## 3. Application Integration

- [x] 3.1 Open `backend/main.py`.
- [x] 3.2 Import the exceptions and handlers from `app.core.exceptions`.
- [x] 3.3 Register the handlers using `app.add_exception_handler(DomainException, domain_exception_handler)` and `app.add_exception_handler(RequestValidationError, validation_exception_handler)`.