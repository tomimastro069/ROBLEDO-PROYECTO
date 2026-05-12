# Auth Specification

## Purpose

This specification defines the core authentication business rules and behaviors within the `auth-service`, abstracting database access via the `UnitOfWork` pattern.

## Requirements

### R1: User Registration
The system MUST allow users to register by hashing their password and persisting the new user using the Unit of Work.

#### Scenario: Successful registration
- GIVEN a valid `UserCreate` payload with a unique email
- WHEN the `AuthService.register` method is called
- THEN the system hashes the password
- AND the system creates a new user record in the database using the `uow.users` repository
- AND the transaction is committed via `uow.commit()`
- AND the method returns the created user (without password hash)

#### Scenario: Duplicate email registration
- GIVEN a valid `UserCreate` payload with an email that already exists
- WHEN the `AuthService.register` method is called
- THEN the `uow.users.get_by_email` returns an existing user
- AND the system raises an `HTTPException` with a 400 Bad Request status

### R2: User Login
The system MUST authenticate users by verifying their credentials against the hashed password and returning a valid JWT.

#### Scenario: Successful login
- GIVEN a valid email and password
- WHEN the `AuthService.login` method is called
- THEN the system retrieves the user using `uow.users.get_by_email`
- AND verifies the password against the stored hash
- AND generates an access JWT and a refresh JWT
- AND returns a `Token` payload

#### Scenario: Invalid credentials
- GIVEN an email and an incorrect password
- WHEN the `AuthService.login` method is called
- THEN password verification fails
- AND the system raises an `HTTPException` with a 401 Unauthorized status

### R3: Token Refresh
The system MUST allow issuing a new access token using a valid refresh token.

#### Scenario: Successful refresh
- GIVEN a valid refresh token
- WHEN the `AuthService.refresh` method is called
- THEN the system decodes and validates the refresh token
- AND retrieves the associated user via `uow.users.get_by_email` or ID
- AND issues a new access token
- AND returns a `Token` payload

### R4: REST API Endpoints
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
