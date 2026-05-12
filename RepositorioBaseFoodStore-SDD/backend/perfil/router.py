from fastapi import APIRouter, Depends, status

from perfil.schemas import PerfilRead, PerfilUpdate, PasswordChange
from perfil.service import PerfilService
from app.core.uow.unit_of_work import AppUnitOfWork, get_uow
from auth.dependencies import get_current_user
from auth.schemas import TokenData

router = APIRouter()


def get_perfil_service(uow: AppUnitOfWork = Depends(get_uow)) -> PerfilService:
    return PerfilService(uow)


@router.get("", response_model=PerfilRead, status_code=status.HTTP_200_OK)
def get_perfil(
    current_user: TokenData = Depends(get_current_user),
    service: PerfilService = Depends(get_perfil_service),
):
    return service.get(int(current_user.sub))


@router.put("", response_model=PerfilRead, status_code=status.HTTP_200_OK)
def update_perfil(
    data: PerfilUpdate,
    current_user: TokenData = Depends(get_current_user),
    service: PerfilService = Depends(get_perfil_service),
):
    return service.update(int(current_user.sub), data)


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(
    data: PasswordChange,
    current_user: TokenData = Depends(get_current_user),
    service: PerfilService = Depends(get_perfil_service),
):
    service.change_password(int(current_user.sub), data)
