from typing import Optional
from sqlmodel import Session, select
from app.core.shared.base_repository import BaseRepository
from app.core.models import User

class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, User)

    def get_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        return self._session.exec(statement).first()

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self._session.get(User, user_id)

    def get_all(self, skip: int = 0, limit: int = 50):
        from sqlmodel import select
        stmt = select(User).offset(skip).limit(limit)
        return list(self._session.exec(stmt).all())

    def count_all(self) -> int:
        from sqlmodel import select, func
        return self._session.exec(select(func.count(User.id))).one()
