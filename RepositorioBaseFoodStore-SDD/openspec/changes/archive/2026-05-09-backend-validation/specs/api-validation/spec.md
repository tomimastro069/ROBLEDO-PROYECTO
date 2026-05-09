# api-validation Specification

## Purpose

Define strict input validation requirements for incoming API requests using dedicated Pydantic schemas (DTOs). This ensures data integrity, proper type casting, and sanitization before data reaches the application controllers and database models.

## ADDED Requirements

### Requirement: User input validation
The system SHALL validate incoming user registration and update data. Passwords MUST meet minimum security criteria and emails MUST be correctly formatted.

#### Scenario: User registration with invalid email
- **GIVEN** a client making a request to register a user
- **WHEN** the email provided is malformed (e.g., "invalid-email")
- **THEN** the system MUST reject the request with a 422 validation error
- **AND** the error response MUST follow RFC 7807 format

#### Scenario: User registration with weak password
- **GIVEN** a client making a request to register a user
- **WHEN** the password is less than 8 characters long
- **THEN** the system MUST reject the request with a 422 validation error

### Requirement: Product input validation
The system SHALL ensure product creation and update requests have semantically correct values. Prices MUST be strictly greater than zero and stock MUST be zero or greater.

#### Scenario: Create product with negative or zero price
- **GIVEN** an admin or gestor making a request to create a product
- **WHEN** the product price is 0 or less
- **THEN** the system MUST reject the request with a 422 validation error

#### Scenario: Create product with negative stock
- **GIVEN** an admin or gestor making a request to create a product
- **WHEN** the product stock is less than 0
- **THEN** the system MUST reject the request with a 422 validation error

### Requirement: Request validation failure response
The system SHALL intercept all Pydantic validation errors (`RequestValidationError`) and format them according to RFC 7807.

#### Scenario: Missing required fields
- **GIVEN** any API endpoint requiring a specific schema payload
- **WHEN** a required field is missing in the request body
- **THEN** the system MUST respond with HTTP status 422
- **AND** the response body MUST contain `invalid_params` array describing the missing fields with their specific reasons
