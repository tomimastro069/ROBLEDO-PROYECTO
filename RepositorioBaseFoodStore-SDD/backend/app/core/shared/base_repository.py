"""
BaseRepository[T] — Generic repository base class.

Design rules:
- Session is injected (never created here).
- NO commit, NO rollback — that belongs to the Unit of Work.
- Operates only within the provided session boundary.
"""

from typing import Generic, TypeVar, Type, Optional, Sequence

from sqlmodel import SQLModel, Session, select

ModelT = TypeVar("ModelT", bound=SQLModel)


class BaseRepository(Generic[ModelT]):
    """
    Generic CRUD repository.

    Usage:
        class UserRepository(BaseRepository[User]):
            def __init__(self, session: Session) -> None:
                super().__init__(session, User)
    """

    def __init__(self, session: Session, model: Type[ModelT]) -> None:
        self._session = session
        self._model = model

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def get_by_id(self, entity_id: int) -> Optional[ModelT]:
        """Return a single entity by primary key, or None if not found."""
        return self._session.get(self._model, entity_id)

    def get_all(self) -> Sequence[ModelT]:
        """Return all rows for this entity."""
        statement = select(self._model)
        return self._session.exec(statement).all()

    # ------------------------------------------------------------------
    # Write  (callers must commit via UoW — never here)
    # ------------------------------------------------------------------

    def add(self, entity: ModelT) -> ModelT:
        """Persist a new entity inside the current session."""
        self._session.add(entity)
        self._session.flush()   # assigns DB-generated id without committing
        self._session.refresh(entity)
        return entity

    def update(self, entity: ModelT) -> ModelT:
        """Merge changes for an already-tracked entity."""
        self._session.add(entity)   # re-attaches detached instances too
        self._session.flush()
        self._session.refresh(entity)
        return entity

    def delete(self, entity: ModelT) -> None:
        """Delete an entity from the database."""
        self._session.delete(entity)
        self._session.flush()
