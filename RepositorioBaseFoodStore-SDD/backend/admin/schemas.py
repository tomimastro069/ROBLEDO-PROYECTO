from typing import Optional, List
from pydantic import BaseModel, Field


class UserAdminRead(BaseModel):
    id: int
    email: str
    name: Optional[str]
    phone: Optional[str]
    is_active: bool
    role_id: Optional[int]

    class Config:
        from_attributes = True


class UserAdminUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=150)
    role_id: Optional[int] = None
    is_active: Optional[bool] = None


class UserAdminCreate(BaseModel):
    email: str
    password: str
    name: str
    role_id: int


class MetricasResumen(BaseModel):
    total_usuarios: int
    total_categorias: int
    total_productos: int


class RoleRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True
