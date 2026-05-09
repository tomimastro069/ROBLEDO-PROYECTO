# Delta for Auth

## ADDED Requirements

### Requirement: REST API Endpoints

The system MUST expose the authentication business logic via standard HTTP REST endpoints.

#### Scenario: Registering via API
- GIVEN a client sends a `POST /auth/register` with a valid JSON body (email, password)
- WHEN the endpoint is hit
- THEN the API MUST respond with HTTP 201 Created
- AND the response body MUST contain the created user details (without password hash)

#### Scenario: Registering with existing email
- GIVEN a client sends a `POST /auth/register` with an already registered email
- WHEN the endpoint is hit
- THEN the API MUST respond with HTTP 400 Bad Request

#### Scenario: Logging in via API
- GIVEN a client sends a `POST /auth/login` with valid credentials (JSON body)
- WHEN the endpoint is hit
- THEN the API MUST respond with HTTP 200 OK
- AND the response MUST include `access_token`, `refresh_token`, and `token_type`

#### Scenario: Refreshing token via API
- GIVEN a client sends a `POST /auth/refresh` with a valid refresh token
- WHEN the endpoint is hit
- THEN the API MUST respond with HTTP 200 OK
- AND the response MUST include new tokens

#### Scenario: Fetching Current User
- GIVEN a client sends a `GET /auth/me` with a valid Bearer token
- WHEN the endpoint is hit
- THEN the API MUST respond with HTTP 200 OK
- AND the response MUST contain the current user data (TokenData payload)

## REMOVED Requirements

### Requirement: Legacy Mock Endpoints

(Reason: The old `backend/app/core/auth.py` containing in-memory hardcoded users must be fully deprecated and its routes unmounted, as real database authentication is now in place).
