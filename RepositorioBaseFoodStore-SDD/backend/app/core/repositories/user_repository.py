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
