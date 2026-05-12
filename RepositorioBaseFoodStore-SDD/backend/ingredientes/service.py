from datetime import datetime, timezone
from typing import List
from fastapi import HTTPException, status

from ingredientes.schemas import IngredienteCreate, IngredienteUpdate
from app.core.uow.unit_of_work import AppUnitOfWork
from app.core.models import Ingrediente


class IngredientesService:
    def __init__(self, uow: AppUnitOfWork) -> None:
        self.uow = uow

    def create(self, data: IngredienteCreate) -> Ingrediente:
        with self.uow as uow:
            if uow.ingredientes.get_by_nombre(data.nombre):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe un ingrediente con el nombre '{data.nombre}'.",
                )
            ingrediente = Ingrediente(nombre=data.nombre, es_alergeno=data.es_alergeno)
            uow.ingredientes.add(ingrediente)
            uow.commit()
            return ingrediente

    def get_all(self) -> List[Ingrediente]:
        with self.uow as uow:
            return uow.ingredientes.get_all_active()

    def get_by_id(self, ingrediente_id: int) -> Ingrediente:
        with self.uow as uow:
            ing = uow.ingredientes.get_by_id_active(ingrediente_id)
            if not ing:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Ingrediente con id={ingrediente_id} no encontrado.",
                )
            return ing

    def update(self, ingrediente_id: int, data: IngredienteUpdate) -> Ingrediente:
        with self.uow as uow:
            ing = uow.ingredientes.get_by_id_active(ingrediente_id)
            if not ing:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Ingrediente con id={ingrediente_id} no encontrado.",
                )
            if data.nombre and data.nombre != ing.nombre:
                if uow.ingredientes.get_by_nombre(data.nombre):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Ya existe un ingrediente con el nombre '{data.nombre}'.",
                    )
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(ing, key, value)
            uow.ingredientes.update(ing)
            uow.commit()
            return ing

    def delete(self, ingrediente_id: int) -> None:
        with self.uow as uow:
            ing = uow.ingredientes.get_by_id_active(ingrediente_id)
            if not ing:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Ingrediente con id={ingrediente_id} no encontrado.",
                )
            ing.deleted_at = datetime.now(timezone.utc)
            uow.ingredientes.update(ing)
            uow.commit()

    def asociar_a_producto(self, product_id: int, ingrediente_id: int) -> None:
        with self.uow as uow:
            ing = uow.ingredientes.get_by_id_active(ingrediente_id)
            if not ing:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingrediente no encontrado.")
            producto = uow.products.get_by_id(product_id)
            if not producto:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado.")
            if uow.ingredientes.link_exists(product_id, ingrediente_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El ingrediente ya está asociado a este producto.",
                )
            uow.ingredientes.add_link(product_id, ingrediente_id)
            uow.commit()

    def desasociar_de_producto(self, product_id: int, ingrediente_id: int) -> None:
        with self.uow as uow:
            if not uow.ingredientes.link_exists(product_id, ingrediente_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="El ingrediente no está asociado a este producto.",
                )
            uow.ingredientes.remove_link(product_id, ingrediente_id)
            uow.commit()

    def get_por_producto(self, product_id: int) -> List[Ingrediente]:
        with self.uow as uow:
            producto = uow.products.get_by_id(product_id)
            if not producto:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado.")
            return uow.ingredientes.get_by_product(product_id)
