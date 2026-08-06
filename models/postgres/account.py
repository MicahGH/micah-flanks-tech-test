from sqlmodel.main import Field

from models.postgres.base_sql_model import BaseSQLModel


class Account(BaseSQLModel, table=True):
    """SQL model for the 'account' table."""

    __tablename__ = "account"  # type: ignore[reportAssignmentType]

    id: int | None = Field(default=None, primary_key=True)
    external_account_id: str = Field(index=True, unique=True)
    entity: str
    iban: str
