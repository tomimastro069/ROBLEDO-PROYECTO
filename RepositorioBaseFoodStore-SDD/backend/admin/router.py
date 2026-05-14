from typing import List
from fastapi import APIRouter, Depends, status

from admin.schemas import UserAdminRead, UserAdminUpdate, UserAdminCreate, MetricasResumen, RoleRead
from admin.service import AdminService
from app.core.uow.unit_of_work import AppUnitOfWork, get_uow
from auth.dependencies import require_role
from auth.roles import Role
from auth.schemas import TokenData

router = APIRouter()


def get_admin_service(uow: AppUnitOfWork = Depends(get_uow)) -> AdminService:
    return AdminService(uow)


# ── Usuarios ──────────────────────────────────────────────────────────────────

@router.get("/usuarios", response_model=List[UserAdminRead], status_code=status.HTTP_200_OK)
def list_users(
    skip: int = 0,
    limit: int = 50,
    current_user: TokenData = Depends(require_role(Role.ADMIN)),
    service: AdminService = Depends(get_admin_service),
):
    return service.list_users(skip=skip, limit=limit)


@router.post("/usuarios", response_model=UserAdminRead, status_code=status.HTTP_201_CREATED)
def create_user(
    data: UserAdminCreate,
    current_user: TokenData = Depends(require_role(Role.ADMIN)),
    service: AdminService = Depends(get_admin_service),
):
    return service.create_user(data)


@router.get("/usuarios/{user_id}", response_model=UserAdminRead, status_code=status.HTTP_200_OK)
def get_user(
    user_id: int,
    current_user: TokenData = Depends(require_role(Role.ADMIN)),
    service: AdminService = Depends(get_admin_service),
):
    return service.get_user(user_id)


@router.put("/usuarios/{user_id}", response_model=UserAdminRead, status_code=status.HTTP_200_OK)
def update_user(
    user_id: int,
    data: UserAdminUpdate,
    current_user: TokenData = Depends(require_role(Role.ADMIN)),
    service: AdminService = Depends(get_admin_service),
):
    return service.update_user(int(current_user.sub), user_id, data)


@router.patch("/usuarios/{user_id}/estado", response_model=UserAdminRead, status_code=status.HTTP_200_OK)
def toggle_user_active(
    user_id: int,
    is_active: bool,
    current_user: TokenData = Depends(require_role(Role.ADMIN)),
    service: AdminService = Depends(get_admin_service),
):
    return service.toggle_active(user_id, is_active)


@router.get("/roles", response_model=List[RoleRead], status_code=status.HTTP_200_OK)
def list_roles(
    current_user: TokenData = Depends(require_role(Role.ADMIN)),
    service: AdminService = Depends(get_admin_service),
):
    return service.list_roles()


# ── Métricas ──────────────────────────────────────────────────────────────────

@router.get("/metricas/resumen", response_model=MetricasResumen, status_code=status.HTTP_200_OK)
def get_metricas_resumen(
    current_user: TokenData = Depends(require_role(Role.ADMIN)),
    service: AdminService = Depends(get_admin_service),
):
    return service.get_resumen()
