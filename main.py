from datetime import date
from typing import Annotated

from fastapi import Depends, FastAPI, File, UploadFile
from sqlmodel import Session

from cache.summary_cache import SummaryCache
from databases.postgres import create_postgres_db, get_postgres_session
from factories.parser_factory import ParserFactory
from models.dataclasses.import_result import ImportResult
from models.postgres.transaction import Transaction
from models.typed_dicts.transactions_summary import TransactionsSummary
from services.transaction_service import TransactionService

app = FastAPI()


@app.on_event("startup")  # type: ignore[reportDeprecated]
def startup() -> None:
    """Execute the tasks on app startup."""
    create_postgres_db()
    app.state.summary_cache = SummaryCache()


@app.post("/transactions/import")
def import_transactions(
    upload_file: Annotated[UploadFile, File(...)],
    pg_session: Annotated[Session, Depends(get_postgres_session)],
) -> ImportResult:
    """Import transactions to the DB from an uploaded file."""
    parser = ParserFactory.create(upload_file=upload_file)

    return TransactionService(
        pg_session=pg_session, cache=app.state.summary_cache
    ).import_transactions(parser=parser)


@app.get("/transactions")
def get_transactions(
    account_id: int,
    from_date: date,
    to_date: date,
    pg_session: Annotated[Session, Depends(get_postgres_session)],
) -> list[Transaction]:
    """Get transactions between provided dates for a provided account."""
    return TransactionService(
        pg_session=pg_session, cache=app.state.summary_cache
    ).get_transactions(
        account_id=account_id,
        from_date=from_date,
        to_date=to_date,
    )


@app.get("/transactions/summary")
def get_transactions_summary(
    account_id: int,
    pg_session: Annotated[Session, Depends(get_postgres_session)],
) -> list[TransactionsSummary]:
    """Get summary of transactions for an account."""
    return TransactionService(
        pg_session=pg_session, cache=app.state.summary_cache
    ).get_transactions_summary(account_id)
