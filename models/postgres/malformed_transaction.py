from datetime import UTC, datetime
from typing import Any

from sqlalchemy.dialects.postgresql import JSON
from sqlmodel import Field

from models.postgres.base_sql_model import BaseSQLModel


class MalformedTransaction(BaseSQLModel, table=True):
    """Malformed transaction received during import."""

    __tablename__ = "malformed_transaction"  # type: ignore[reportAssignmentType]

    raw_data: dict[str, Any] = Field(sa_type=JSON)
    errors: list[dict[str, Any]] = Field(sa_type=JSON)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )
