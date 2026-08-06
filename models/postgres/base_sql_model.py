from sqlmodel import Field, SQLModel


class BaseSQLModel(SQLModel):
    """Base SQL model for the Postgres tables."""

    id: int | None = Field(default=None, primary_key=True)
