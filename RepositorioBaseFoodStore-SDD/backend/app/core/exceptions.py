from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import Any

# ==========================================
# Domain Exceptions
# ==========================================

class DomainException(Exception):
    """Base class for business logic exceptions mapped to RFC 7807."""
    def __init__(self, title: str, detail: str, status_code: int = 400, error_type: str = "about:blank"):
        self.title = title
        self.detail = detail
        self.status_code = status_code
        self.error_type = error_type

class NotFoundException(DomainException):
    def __init__(self, detail: str = "Recurso no encontrado"):
        super().__init__(
            title="Not Found",
            detail=detail,
            status_code=404,
            error_type="https://api.foodstore.com/errors/not-found"
        )

class BadRequestException(DomainException):
    def __init__(self, detail: str = "Petición inválida"):
        super().__init__(
            title="Bad Request",
            detail=detail,
            status_code=400,
            error_type="https://api.foodstore.com/errors/bad-request"
        )

class UnauthorizedException(DomainException):
    def __init__(self, detail: str = "No autorizado"):
        super().__init__(
            title="Unauthorized",
            detail=detail,
            status_code=401,
            error_type="https://api.foodstore.com/errors/unauthorized"
        )

# ==========================================
# FastAPI Handlers
# ==========================================

async def domain_exception_handler(request: Request, exc: DomainException) -> JSONResponse:
    """Catches DomainException and formats it as an RFC 7807 JSONResponse."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "type": exc.error_type,
            "title": exc.title,
            "status": exc.status_code,
            "detail": exc.detail,
            "instance": str(request.url)
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Intercepts FastAPI RequestValidationError and formats it as RFC 7807 with invalid_params."""
    invalid_params = [{"field": ".".join(map(str, err.get("loc", []))), "reason": err.get("msg")} for err in exc.errors()]
    
    return JSONResponse(
        status_code=422,
        content={
            "type": "https://api.foodstore.com/errors/validation-error",
            "title": "Validation Error",
            "status": 422,
            "detail": "Los datos enviados no son válidos. Revisa el campo 'invalid_params'.",
            "instance": str(request.url),
            "invalid_params": invalid_params
        }
    )
