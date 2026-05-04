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

from sqlmodel import Session, create_engine

# Motor compartido — en producción se leerá de config/env
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# La base de datos está un nivel arriba, en la carpeta backend/
_DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, '..', 'database.db')}"
_engine = create_engine(_DATABASE_URL, echo=False)


def get_engine():
    """Devuelve el engine global. Reemplazar en tests con uno in-memory."""
    return _engine


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
        self.session = Session(self._engine)
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
