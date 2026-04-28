"""
Token schema — payload que vive dentro del JWT.

TokenData es lo que se decodifica del Bearer token y se pasa
a get_current_user para hidratar el usuario activo.
"""

from typing import Optional
from pydantic import BaseModel
from auth.roles import Role


class TokenData(BaseModel):
    sub: str                    # user_id como string (estándar JWT)
    role: Role
    email: Optional[str] = None
