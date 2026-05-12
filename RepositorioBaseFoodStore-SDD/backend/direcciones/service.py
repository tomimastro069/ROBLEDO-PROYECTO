from typing import List
from fastapi import HTTPException, status

from direcciones.schemas import AddressCreate, AddressUpdate
from app.core.uow.unit_of_work import AppUnitOfWork
from app.core.models import Address


class DireccionesService:
    def __init__(self, uow: AppUnitOfWork) -> None:
        self.uow = uow

    def create(self, user_id: int, data: AddressCreate) -> Address:
        with self.uow as uow:
            is_first = uow.addresses.count_by_user(user_id) == 0
            address = Address(
                **data.model_dump(),
                user_id=user_id,
                is_default=is_first,
            )
            uow.addresses.add(address)
            uow.commit()
            return address

    def list_by_user(self, user_id: int) -> List[Address]:
        with self.uow as uow:
            return uow.addresses.get_by_user(user_id)

    def update(self, user_id: int, address_id: int, data: AddressUpdate) -> Address:
        with self.uow as uow:
            address = uow.addresses.get_user_address(user_id, address_id)
            if not address:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dirección no encontrada.")
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(address, key, value)
            uow.addresses.update(address)
            uow.commit()
            return address

    def delete(self, user_id: int, address_id: int) -> None:
        with self.uow as uow:
            address = uow.addresses.get_user_address(user_id, address_id)
            if not address:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dirección no encontrada.")
            was_default = address.is_default
            uow.addresses.delete(address)
            uow.commit()
            if was_default:
                remaining = uow.addresses.get_by_user(user_id)
                if remaining:
                    remaining[0].is_default = True
                    uow.addresses.update(remaining[0])
                    uow.commit()

    def set_default(self, user_id: int, address_id: int) -> Address:
        with self.uow as uow:
            address = uow.addresses.get_user_address(user_id, address_id)
            if not address:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dirección no encontrada.")
            uow.addresses.clear_default(user_id)
            address.is_default = True
            uow.addresses.update(address)
            uow.commit()
            return address
