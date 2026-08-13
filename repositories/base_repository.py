from collections.abc import Iterable
from typing import TypeVar

from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session, SQLModel, select

from models.enums.upsert_result import UpsertResult
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

    def insert_on_conflict_do_update(
        self,
        model: type[BaseSQLModel],
        values: dict[str, object],
        conflict_columns: list[str],
    ) -> UpsertResult:
        """Insert a record or update it if it already exists."""
        conflict_values = {column: values[column] for column in conflict_columns}
        existing = self._session.exec(
            select(model).filter_by(**conflict_values)
        ).first()

        statement = insert(model).values(values)

        update_values = {
            key: value for key, value in values.items() if key not in conflict_columns
        }

        statement = statement.on_conflict_do_update(
            index_elements=conflict_columns,
            set_=update_values,
        )

        self._session.exec(statement)

        return UpsertResult.UPDATED if existing else UpsertResult.INSERTED
