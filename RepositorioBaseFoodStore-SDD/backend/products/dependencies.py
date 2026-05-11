"""
Dependency injection for Products module.

Main exports:
  - get_products_service → Injectable that returns ProductsService instance
"""

from fastapi import Depends

from app.core.uow.unit_of_work import AppUnitOfWork, get_uow
from products.service import ProductsService


def get_products_service(uow: AppUnitOfWork = Depends(get_uow)) -> ProductsService:
    """
    Injects the products service layer instantiated with the active UnitOfWork.
    
    Usage in a router:
        @router.get("/products")
        def list_products(service: ProductsService = Depends(get_products_service)):
            return service.get_all()
    """
    return ProductsService(uow)
