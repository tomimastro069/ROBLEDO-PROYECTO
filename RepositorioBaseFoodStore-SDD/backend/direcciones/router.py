from typing import List
from fastapi import APIRouter, Depends, status

from direcciones.schemas import AddressCreate, AddressUpdate, AddressRead
from direcciones.service import DireccionesService
from direcciones.dependencies import get_direcciones_service
from auth.dependencies import get_current_user
from auth.schemas import TokenData

router = APIRouter()


@router.get("", response_model=List[AddressRead], status_code=status.HTTP_200_OK)
def list_addresses(
    current_user: TokenData = Depends(get_current_user),
    service: DireccionesService = Depends(get_direcciones_service),
):
    return service.list_by_user(int(current_user.sub))


@router.post("", response_model=AddressRead, status_code=status.HTTP_201_CREATED)
def create_address(
    data: AddressCreate,
    current_user: TokenData = Depends(get_current_user),
    service: DireccionesService = Depends(get_direcciones_service),
):
    return service.create(int(current_user.sub), data)


@router.put("/{address_id}", response_model=AddressRead, status_code=status.HTTP_200_OK)
def update_address(
    address_id: int,
    data: AddressUpdate,
    current_user: TokenData = Depends(get_current_user),
    service: DireccionesService = Depends(get_direcciones_service),
):
    return service.update(int(current_user.sub), address_id, data)


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(
    address_id: int,
    current_user: TokenData = Depends(get_current_user),
    service: DireccionesService = Depends(get_direcciones_service),
):
    service.delete(int(current_user.sub), address_id)


@router.patch("/{address_id}/predeterminada", response_model=AddressRead, status_code=status.HTTP_200_OK)
def set_default_address(
    address_id: int,
    current_user: TokenData = Depends(get_current_user),
    service: DireccionesService = Depends(get_direcciones_service),
):
    return service.set_default(int(current_user.sub), address_id)
