from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from auth.schemas import UserCreate, UserLogin, Token, TokenData
from auth.service import AuthService
from auth.dependencies import get_auth_service, get_current_user
from app.core.models import User

router = APIRouter()

# Schema para la respuesta del register para no devolver el hash de password
class UserResponse(BaseModel):
    id: int
    email: str
    
    class Config:
        from_attributes = True

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    user = auth_service.register(user_in)
    return user

@router.post("/login", response_model=Token)
def login(user_in: UserLogin, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.login(user_in.email, user_in.password)

class RefreshRequest(BaseModel):
    refresh_token: str

@router.post("/refresh", response_model=Token)
def refresh(request: RefreshRequest, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.refresh(request.refresh_token)

@router.get("/me", response_model=TokenData)
def read_users_me(current_user: TokenData = Depends(get_current_user)):
    return current_user
