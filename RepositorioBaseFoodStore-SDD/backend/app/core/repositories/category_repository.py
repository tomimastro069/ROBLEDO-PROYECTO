from typing import Optional, List
from sqlmodel import Session, select
from app.core.shared.base_repository import BaseRepository
from app.core.models import Category


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Category)

    def get_by_name(self, name: str) -> Optional[Category]:
        statement = select(Category).where(Category.name == name)
        return self._session.exec(statement).first()

    def get_root_categories(self) -> List[Category]:
        """Retorna solo las categorías raíz (sin parent)."""
        statement = select(Category).where(Category.parent_id == None)  # noqa: E711
        return list(self._session.exec(statement).all())

    def get_children(self, parent_id: int) -> List[Category]:
        """Retorna las subcategorías directas de un parent."""
        statement = select(Category).where(Category.parent_id == parent_id)
        return list(self._session.exec(statement).all())
