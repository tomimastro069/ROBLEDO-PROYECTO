from fastapi import HTTPException, status
from jose import JWTError, jwt

from auth.schemas import UserCreate, UserLogin, Token
from auth.utils import get_password_hash, verify_password, create_access_token, create_refresh_token, SECRET_KEY, ALGORITHM
from app.core.uow.unit_of_work import AppUnitOfWork
from app.core.models import User

class AuthService:
    def __init__(self, uow: AppUnitOfWork):
        self.uow = uow

    def register(self, user_in: UserCreate) -> User:
        with self.uow as uow:
            existing_user = uow.users.get_by_email(user_in.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            
            # Retrieve default role (e.g. 'user') if possible
            # role = uow.roles.get_by_name("user") # Omitted to simplify, will just use role_id=None or whatever is default

            hashed_password = get_password_hash(user_in.password)
            new_user = User(
                email=user_in.email,
                hashed_password=hashed_password,
                # first_name and last_name not in models yet
            )
            
            uow.users.add(new_user)
            # uow.commit() called implicitly upon exit of 'with', but specs say "AND the transaction is committed via uow.commit()"
            uow.commit() 
            return new_user

    def login(self, email: str, password: str) -> Token:
        with self.uow as uow:
            user = uow.users.get_by_email(email)
            if not user or not verify_password(password, user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # we need user.role but role might be None. we assume user.role.name for the token if role is loaded
            role_name = user.role.name if user.role else "user"

            access_token = create_access_token(
                data={"sub": str(user.id), "email": user.email, "role": role_name}
            )
            refresh_token = create_refresh_token(
                data={"sub": str(user.id), "email": user.email, "role": role_name}
            )
            
            return Token(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer"
            )

    def refresh(self, refresh_token: str) -> Token:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id_str: str = payload.get("sub")
            if user_id_str is None:
                raise credentials_exception
            user_id = int(user_id_str)
        except (JWTError, ValueError):
            raise credentials_exception

        with self.uow as uow:
            user = uow.users.get(user_id)
            if user is None:
                raise credentials_exception
            
            role_name = user.role.name if user.role else "user"
            
            access_token = create_access_token(
                data={"sub": str(user.id), "email": user.email, "role": role_name}
            )
            new_refresh_token = create_refresh_token(
                data={"sub": str(user.id), "email": user.email, "role": role_name}
            )
            
            return Token(
                access_token=access_token,
                refresh_token=new_refresh_token,
                token_type="bearer"
            )
