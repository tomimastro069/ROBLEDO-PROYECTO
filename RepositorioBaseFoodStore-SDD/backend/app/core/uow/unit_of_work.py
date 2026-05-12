"""
Unit of Work — gestiona el ciclo de vida de la sesión y la transacción.

Responsabilidades:
  - Abre la sesión de DB al entrar al contexto.
  - Hace commit si todo salió bien.
  - Hace rollback si ocurre cualquier excepción.
  - Cierra la sesión al salir (siempre).

Uso desde un servicio:
    with UnitOfWork() as uow:
        user = uow.users.add(User(name="Ana"))
        # commit automático al salir del with sin excepción

Diseño: el UoW crea los repositorios concretos con la misma sesión
para garantizar atomicidad — todos operan dentro de la misma transacción.
"""

from __future__ import annotations

from sqlmodel import Session
from app.core.database import engine as global_engine
from app.core.repositories.user_repository import UserRepository
from app.core.repositories.role_repository import RoleRepository
from app.core.repositories.category_repository import CategoryRepository
from app.core.repositories.products_repository import ProductsRepository
from app.core.repositories.product_ingredient_repository import ProductIngredientRepository
from app.core.repositories.product_allergen_repository import ProductAllergenRepository
from app.core.repositories.address_repository import AddressRepository
from app.core.repositories.ingrediente_repository import IngredienteRepository

def get_engine():
    """Devuelve el engine global. Reemplazar en tests con uno in-memory."""
    return global_engine


class UnitOfWork:
    """
    Context manager que encapsula una transacción completa.

    Extiende esta clase en cada módulo para agregar los repositorios
    concretos que ese módulo necesita:

        class UserUnitOfWork(UnitOfWork):
            def __enter__(self):
                super().__enter__()
                self.users = UserRepository(self.session)
                return self
    """

    def __init__(self, engine=None) -> None:
        self._engine = engine or get_engine()

    def __enter__(self) -> "UnitOfWork":
        self.session = Session(self._engine, expire_on_commit=False)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        try:
            if exc_type is None:
                self.session.commit()
            else:
                self.session.rollback()
        finally:
            self.session.close()
        # Propaga la excepción original (no la suprime)
        return False

    # ------------------------------------------------------------------
    # Helpers opcionales para uso explícito dentro del with
    # ------------------------------------------------------------------

    def commit(self) -> None:
        """Commit explícito dentro del contexto (ej: commits intermedios)."""
        self.session.commit()

    def rollback(self) -> None:
        """Rollback explícito ante errores de negocio."""
        self.session.rollback()

class AppUnitOfWork(UnitOfWork):
    def __enter__(self) -> "AppUnitOfWork":
        super().__enter__()
        self.users = UserRepository(self.session)
        self.roles = RoleRepository(self.session)
        self.categories = CategoryRepository(self.session)
        self.products = ProductsRepository(self.session)
        self.product_ingredients = ProductIngredientRepository(self.session)
        self.product_allergens = ProductAllergenRepository(self.session)
        self.addresses = AddressRepository(self.session)
        self.ingredientes = IngredienteRepository(self.session)
        return self

def get_uow() -> AppUnitOfWork:
    return AppUnitOfWork()
