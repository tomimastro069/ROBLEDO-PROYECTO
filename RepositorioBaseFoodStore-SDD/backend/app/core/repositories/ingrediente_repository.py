from typing import List, Optional
from sqlmodel import Session, select
from app.core.shared.base_repository import BaseRepository
from app.core.models import Ingrediente, ProductIngrediente


class IngredienteRepository(BaseRepository[Ingrediente]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Ingrediente)

    def get_all_active(self) -> List[Ingrediente]:
        stmt = select(Ingrediente).where(Ingrediente.deleted_at.is_(None))
        return list(self._session.exec(stmt).all())

    def get_by_id_active(self, ingrediente_id: int) -> Optional[Ingrediente]:
        stmt = select(Ingrediente).where(
            Ingrediente.id == ingrediente_id,
            Ingrediente.deleted_at.is_(None),
        )
        return self._session.exec(stmt).first()

    def get_by_nombre(self, nombre: str) -> Optional[Ingrediente]:
        stmt = select(Ingrediente).where(
            Ingrediente.nombre == nombre,
            Ingrediente.deleted_at.is_(None),
        )
        return self._session.exec(stmt).first()

    def get_por_producto(self, product_id: int) -> List[Ingrediente]:
        stmt = (
            select(Ingrediente)
            .join(ProductIngrediente, ProductIngrediente.ingrediente_id == Ingrediente.id)
            .where(ProductIngrediente.product_id == product_id)
            .where(Ingrediente.deleted_at.is_(None))
        )
        return list(self._session.exec(stmt).all())

    def link_exists(self, product_id: int, ingrediente_id: int) -> bool:
        stmt = select(ProductIngrediente).where(
            ProductIngrediente.product_id == product_id,
            ProductIngrediente.ingrediente_id == ingrediente_id,
        )
        return self._session.exec(stmt).first() is not None

    def add_link(self, product_id: int, ingrediente_id: int) -> ProductIngrediente:
        link = ProductIngrediente(product_id=product_id, ingrediente_id=ingrediente_id)
        self._session.add(link)
        self._session.flush()
        return link

    def remove_link(self, product_id: int, ingrediente_id: int) -> None:
        stmt = select(ProductIngrediente).where(
            ProductIngrediente.product_id == product_id,
            ProductIngrediente.ingrediente_id == ingrediente_id,
        )
        link = self._session.exec(stmt).first()
        if link:
            self._session.delete(link)
            self._session.flush()
