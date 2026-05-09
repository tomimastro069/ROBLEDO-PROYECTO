from typing import Optional
from pydantic import BaseModel, EmailStr, Field

from app.schemas.base import ORMBaseModel

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, description="Password must be at least 8 characters long")
    role_id: Optional[int] = None

class UserRead(ORMBaseModel):
    id: int
    email: EmailStr
    role_id: Optional[int] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=8)
    role_id: Optional[int] = None
