"""
Dependencias de inyección para Categories.

Exports principales:
  - get_categories_service  → inyectable que retorna una instancia de CategoriesService
"""

from fastapi import Depends

from app.core.uow.unit_of_work import AppUnitOfWork, get_uow
from categories.service import CategoriesService


def get_categories_service(uow: AppUnitOfWork = Depends(get_uow)) -> CategoriesService:
    """
    Inyecta la capa de servicio de categorías instanciada con el UnitOfWork activo.
    """
    return CategoriesService(uow)
