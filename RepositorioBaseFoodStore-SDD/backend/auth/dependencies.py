"""
Dependencias de autenticación y autorización para FastAPI.

Exports principales:
  - get_current_user  → inyectable que retorna el TokenData del usuario activo
  - require_role()    → factory que retorna un inyectable que verifica roles

Uso en un router:
    @router.get("/admin/dashboard")
    def admin_dashboard(
        current_user: TokenData = Depends(require_role(Role.ADMIN))
    ):
        ...

    @router.get("/me")
    def profile(current_user: TokenData = Depends(get_current_user)):
        ...

Configuración (leer de .env en producción):
    AUTH_SECRET_KEY   — clave secreta para firmar JWT
    AUTH_ALGORITHM    — algoritmo (default: HS256)
"""

import os
from typing import List

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from auth.roles import Role
from auth.schemas import TokenData
from app.core.config import settings

SECRET_KEY: str = settings.SECRET_KEY
ALGORITHM: str = os.getenv("AUTH_ALGORITHM", "HS256")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# ------------------------------------------------------------------
# get_current_user
# ------------------------------------------------------------------

def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    """
    FastAPI dependency — decodifica el Bearer token y retorna TokenData.

    Lanza HTTP 401 si el token es inválido, expirado o malformado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autenticado o token inválido.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        role_str: str = payload.get("role")

        if user_id is None or role_str is None:
            raise credentials_exception

        token_data = TokenData(sub=user_id, role=Role(role_str), email=payload.get("email"))
    except (JWTError, ValueError):
        raise credentials_exception

    return token_data


# ------------------------------------------------------------------
# require_role — factory de dependencias por rol
# ------------------------------------------------------------------

def require_role(*allowed_roles: Role):
    """
    Factory que devuelve una dependencia FastAPI que verifica roles.

    Acepta uno o más roles permitidos (OR semántico).

    Ejemplos:
        Depends(require_role(Role.ADMIN))
        Depends(require_role(Role.ADMIN, Role.GESTOR_STOCK))
    """
    allowed: List[Role] = list(allowed_roles)

    def _check_role(current_user: TokenData = Depends(get_current_user)) -> TokenData:
        if current_user.role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Roles requeridos: {[r.value for r in allowed]}.",
            )
        return current_user

    return _check_role

# ------------------------------------------------------------------
# get_auth_service
# ------------------------------------------------------------------
from app.core.uow.unit_of_work import AppUnitOfWork, get_uow
from auth.service import AuthService

def get_auth_service(uow: AppUnitOfWork = Depends(get_uow)) -> AuthService:
    """
    Inyecta la capa de servicio de autenticación instanciada con el UnitOfWork activo.
    """
    return AuthService(uow)
