from sqlmodel.main import Field, SQLModel


class Account(SQLModel, table=True):
    """SQL model for the 'account' table."""

    __tablename__ = "account"  # type: ignore[reportAssignmentType]

    id: int | None = Field(default=None, primary_key=True)
    account_id: str = Field(index=True, unique=True)
    entity: str
    iban: str
