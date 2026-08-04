import os
from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(
    DATABASE_URL,
    echo=False,
)


def get_postgres_session() -> Generator[Session]:
    """Yields a new session."""
    with Session(engine) as session:
        yield session


def create_postgres_db() -> None:
    """Create the Postgres DB."""
    SQLModel.metadata.create_all(engine)
