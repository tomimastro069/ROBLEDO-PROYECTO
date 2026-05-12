from typing import List, Optional
from sqlmodel import Session, select
from app.core.shared.base_repository import BaseRepository
from app.core.models import Address


class AddressRepository(BaseRepository[Address]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Address)

    def get_by_user(self, user_id: int) -> List[Address]:
        stmt = select(Address).where(Address.user_id == user_id, Address.order_id.is_(None))
        return list(self._session.exec(stmt).all())

    def get_user_address(self, user_id: int, address_id: int) -> Optional[Address]:
        stmt = select(Address).where(Address.id == address_id, Address.user_id == user_id)
        return self._session.exec(stmt).first()

    def get_default(self, user_id: int) -> Optional[Address]:
        stmt = select(Address).where(Address.user_id == user_id, Address.is_default.is_(True))
        return self._session.exec(stmt).first()

    def count_by_user(self, user_id: int) -> int:
        return len(self.get_by_user(user_id))

    def clear_default(self, user_id: int) -> None:
        for addr in self.get_by_user(user_id):
            if addr.is_default:
                addr.is_default = False
                self._session.add(addr)
        self._session.flush()
