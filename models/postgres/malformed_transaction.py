from datetime import UTC, datetime
from typing import Any

from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field

from models.postgres.base_sql_model import BaseSQLModel


class MalformedTransaction(BaseSQLModel, table=True):
    """Malformed transaction received during import."""

    raw_data: dict[str, Any] = Field(sa_type=JSONB)
    errors: list[dict[str, Any]] = Field(sa_type=JSONB)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )
