from collections.abc import Iterable
from typing import Any, TypeVar

from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session, SQLModel

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

    def insert_on_conflict_do_nothing(
        self,
        model: type[SQLModel],
        values: dict[str, Any],
        conflict_columns: list[str],
    ) -> bool:
        """Insert the record, if there is not a conflict else ignore it."""
        stmt = (
            insert(model)
            .values(**values)
            .on_conflict_do_nothing(index_elements=conflict_columns)
        )

        result = self._session.exec(stmt)
        return result.rowcount == 1
