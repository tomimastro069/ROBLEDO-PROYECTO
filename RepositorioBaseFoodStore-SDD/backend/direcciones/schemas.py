from typing import Optional
from pydantic import BaseModel, Field


class AddressBase(BaseModel):
    street: str = Field(..., min_length=1, max_length=200)
    numero: Optional[str] = Field(None, max_length=20)
    piso: Optional[str] = Field(None, max_length=20)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=1, max_length=100)
    zip_code: str = Field(..., min_length=1, max_length=20)


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    street: Optional[str] = Field(None, min_length=1, max_length=200)
    numero: Optional[str] = Field(None, max_length=20)
    piso: Optional[str] = Field(None, max_length=20)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, min_length=1, max_length=100)
    zip_code: Optional[str] = Field(None, min_length=1, max_length=20)


class AddressRead(AddressBase):
    id: int
    is_default: bool

    class Config:
        from_attributes = True
