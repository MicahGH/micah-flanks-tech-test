from typing import TYPE_CHECKING, TypeVar

from sqlmodel import Session, SQLModel

if TYPE_CHECKING:
    from collections.abc import Iterable

T = TypeVar("T", bound=SQLModel)


class BaseRepository[T: SQLModel]:
    """Base repository with common operations."""

    def __init__(self, pg_session: Session) -> None:
        self._session = pg_session

    def save(self, entity: T) -> None:
        """Save an entity to the DB."""
        self._session.add(entity)

    def save_all(self, entities: Iterable[T]) -> None:
        """Save multiple entities to the DB."""
        self._session.add_all(entities)

    def commit(self) -> None:
        """Commit the changes."""
        self._session.commit()

    def refresh(self, entity: T) -> None:
        """Refresh a provided entity."""
        self._session.refresh(entity)
