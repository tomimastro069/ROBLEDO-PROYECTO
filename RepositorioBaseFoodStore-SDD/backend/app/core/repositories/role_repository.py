from typing import Optional
from sqlmodel import Session, select
from app.core.shared.base_repository import BaseRepository
from app.core.models import Role

class RoleRepository(BaseRepository[Role]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Role)

    def get_by_name(self, name: str) -> Optional[Role]:
        statement = select(Role).where(Role.name == name)
        return self._session.exec(statement).first()
