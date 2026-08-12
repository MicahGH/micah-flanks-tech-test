from collections.abc import Iterable
from typing import Any, TypeVar

from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session, SQLModel, col

from models.postgres.base_sql_model import BaseSQLModel

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
        model: type[BaseSQLModel],
        values: dict[str, Any],
        conflict_columns: list[str],
    ) -> bool:
        """Insert the record, if there is not a conflict else ignore it."""
        stmt = (
            insert(model)
            .values(**values)
            .on_conflict_do_nothing(index_elements=conflict_columns)
            .returning(col(model.id))
        )

        result = self._session.exec(stmt)

        return result.first() is not None

    def insert_on_conflict_do_update(
        self,
        model: type[BaseSQLModel],
        values: dict[str, object],
        conflict_columns: list[str],
    ) -> bool:
        """Insert a transaction or update it if it already exists."""
        statement = insert(model).values(values)

        update_values = {
            key: value for key, value in values.items() if key not in conflict_columns
        }

        statement = statement.on_conflict_do_update(
            index_elements=conflict_columns,
            set_=update_values,
        )

        statement = statement.returning(col(model.id))

        result = self._session.exec(statement)

        return result.first() is not None
