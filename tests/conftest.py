from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from cache.summary_cache import SummaryCache
from main import app
from services.transaction_service import TransactionService


@pytest.fixture
def client() -> Generator[TestClient]:
    """Fixture for the FastAPI test client."""
    with TestClient(app) as client:
        yield client


@pytest.fixture
def session() -> Generator[Session]:
    """Fixture for the postgres session."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture
def transaction_service(session: Session) -> TransactionService:
    """Fixture for transaction serivce."""
    cache = SummaryCache()

    return TransactionService(
        pg_session=session,
        cache=cache,
    )
