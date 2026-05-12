from fastapi import Depends
from app.core.uow.unit_of_work import AppUnitOfWork, get_uow
from direcciones.service import DireccionesService


def get_direcciones_service(uow: AppUnitOfWork = Depends(get_uow)) -> DireccionesService:
    return DireccionesService(uow)
