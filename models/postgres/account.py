from sqlmodel.main import Field

from models.postgres.base_sql_model import BaseSQLModel


class Account(BaseSQLModel, table=True):
    """SQL model for the 'account' table."""

    __tablename__ = "account"  # type: ignore[reportAssignmentType]

    external_account_id: str = Field(index=True, unique=True)
    entity: str
    iban: str
