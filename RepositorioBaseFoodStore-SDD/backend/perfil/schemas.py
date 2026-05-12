from typing import Optional
from pydantic import BaseModel, Field


class PerfilRead(BaseModel):
    id: int
    email: str
    name: Optional[str]
    phone: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True


class PerfilUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    phone: Optional[str] = Field(None, max_length=30)


class PasswordChange(BaseModel):
    password_actual: str = Field(..., min_length=1)
    password_nueva: str = Field(..., min_length=8)
