from fastapi import HTTPException, status

from perfil.schemas import PerfilUpdate, PasswordChange
from app.core.uow.unit_of_work import AppUnitOfWork
from app.core.models import User
from auth.utils import verify_password, get_password_hash


class PerfilService:
    def __init__(self, uow: AppUnitOfWork) -> None:
        self.uow = uow

    def get(self, user_id: int) -> User:
        with self.uow as uow:
            user = uow.users.get_by_id(user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")
            return user

    def update(self, user_id: int, data: PerfilUpdate) -> User:
        with self.uow as uow:
            user = uow.users.get_by_id(user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(user, key, value)
            uow.users.update(user)
            uow.commit()
            return user

    def change_password(self, user_id: int, data: PasswordChange) -> None:
        with self.uow as uow:
            user = uow.users.get_by_id(user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")
            if not verify_password(data.password_actual, user.hashed_password):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Contraseña actual incorrecta.")
            user.hashed_password = get_password_hash(data.password_nueva)
            uow.users.update(user)
            uow.commit()
