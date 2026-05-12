"""
CategoriesService — lógica de negocio para categorías jerárquicas.

Responsabilidades:
  - CRUD de categorías.
  - Validación de reglas de dominio: unicidad de nombre, ciclos jerárquicos.
  - Coordinación de transacciones vía UoW.
  - Soft delete: marcar categorías como eliminadas (no borrar física).

No contiene lógica HTTP. El router del change #14 lo consume vía DI.
"""

from datetime import datetime, timezone
from fastapi import HTTPException, status

from categories.schemas import CategoryCreate, CategoryUpdate, CategoryRead
from app.core.uow.unit_of_work import AppUnitOfWork
from app.core.models import Category


class CategoriesService:
    def __init__(self, uow: AppUnitOfWork) -> None:
        self.uow = uow

    def create(self, data: CategoryCreate) -> Category:
        with self.uow as uow:
            # Regla: nombre único por nivel
            existing = uow.categories.get_by_name(data.name)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe una categoría con el nombre '{data.name}'.",
                )

            # Regla: el parent debe existir si se especifica
            if data.parent_id is not None:
                parent = uow.categories.get_by_id(data.parent_id)
                if not parent:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Categoría padre con id={data.parent_id} no encontrada.",
                    )

            category = Category(**data.model_dump())
            uow.categories.add(category)
            uow.commit()
            return category

    def get_all(self) -> list[Category]:
        with self.uow as uow:
            return list(uow.categories.get_all())

    def get_by_id(self, category_id: int) -> Category:
        with self.uow as uow:
            category = uow.categories.get_by_id(category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Categoría con id={category_id} no encontrada.",
                )
            return category

    def get_tree(self) -> list[Category]:
        """Retorna solo categorías raíz. Las subcategorías se anidan vía relación ORM."""
        with self.uow as uow:
            return uow.categories.get_root_categories()

    def update(self, category_id: int, data: CategoryUpdate) -> Category:
        with self.uow as uow:
            category = uow.categories.get_by_id(category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Categoría con id={category_id} no encontrada.",
                )

            # Regla: no permitir auto-referencia
            if data.parent_id is not None and data.parent_id == category_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Una categoría no puede ser su propio padre.",
                )

            # Regla: el nuevo parent debe existir
            if data.parent_id is not None:
                parent = uow.categories.get_by_id(data.parent_id)
                if not parent:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Categoría padre con id={data.parent_id} no encontrada.",
                    )

            update_data = data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(category, key, value)

            uow.categories.update(category)
            uow.commit()
            return category

    def delete(self, category_id: int) -> None:
        """
        Soft-delete a category by marking it as deleted.
        
        The category is not physically removed from the database,
        but marked with a deleted_at timestamp for auditing and recovery.
        """
        with self.uow as uow:
            category = uow.categories.get_by_id(category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Categoría con id={category_id} no encontrada.",
                )

            # Regla: no eliminar si tiene subcategorías activas
            children = uow.categories.get_children(category_id)
            if children:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="No se puede eliminar una categoría que tiene subcategorías. Eliminá primero las subcategorías.",
                )

            # Soft delete: marcar con timestamp
            category.deleted_at = datetime.now(timezone.utc)
            uow.categories.update(category)
            uow.commit()
