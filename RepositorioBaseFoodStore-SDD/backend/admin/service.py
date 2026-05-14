from typing import List
from fastapi import HTTPException, status

from admin.schemas import UserAdminUpdate, UserAdminCreate, MetricasResumen
from app.core.uow.unit_of_work import AppUnitOfWork
from app.core.models import User, Role
from auth.utils import get_password_hash


class AdminService:
    def __init__(self, uow: AppUnitOfWork) -> None:
        self.uow = uow

    # --- Usuarios ---

    def list_users(self, skip: int = 0, limit: int = 50) -> List[User]:
        with self.uow as uow:
            return uow.users.get_all(skip=skip, limit=limit)

    def create_user(self, data: UserAdminCreate) -> User:
        with self.uow as uow:
            # Verificar si ya existe el email
            existing = uow.users.get_by_email(data.email)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe un usuario con ese email."
                )
            
            user = User(
                email=data.email,
                hashed_password=get_password_hash(data.password),
                name=data.name,
                role_id=data.role_id,
                is_active=True
            )
            uow.users.add(user)
            uow.commit()
            return user

    def get_user(self, user_id: int) -> User:
        with self.uow as uow:
            user = uow.users.get_by_id(user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")
            return user

    def update_user(self, admin_id: int, user_id: int, data: UserAdminUpdate) -> User:
        with self.uow as uow:
            user = uow.users.get_by_id(user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")
            # Regla: admin no puede quitarse el rol a sí mismo
            if user_id == admin_id and data.role_id is not None:
                admin_role = uow.roles.get_by_name("admin")
                if admin_role and user.role_id == admin_role.id and data.role_id != admin_role.id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Un Admin no puede quitarse el rol ADMIN a sí mismo.",
                    )
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(user, key, value)
            uow.users.update(user)
            uow.commit()
            return user

    def toggle_active(self, user_id: int, is_active: bool) -> User:
        with self.uow as uow:
            user = uow.users.get_by_id(user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")
            user.is_active = is_active
            uow.users.update(user)
            uow.commit()
            return user

    def list_roles(self) -> List[Role]:
        with self.uow as uow:
            return uow.roles.get_all()

    # --- Métricas ---

    def get_resumen(self) -> MetricasResumen:
        with self.uow as uow:
            total_usuarios = uow.users.count_all()
            total_categorias = len(uow.categories.get_all())
            total_productos = len(uow.products.get_all())
            return MetricasResumen(
                total_usuarios=total_usuarios,
                total_categorias=total_categorias,
                total_productos=total_productos,
            )
