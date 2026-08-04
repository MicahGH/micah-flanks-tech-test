from http.client import OK
from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, FastAPI, File, UploadFile

from databases.postgres import create_postgres_db, get_postgres_session
from factories.parser_factory import ParserFactory
from services.transaction_service import TransactionService

if TYPE_CHECKING:
    from datetime import date

    from sqlmodel import Session

    from models.postgres.transaction import Transaction
    from models.typed_dicts.transactions_summary import TransactionsSummary

app = FastAPI()


@app.on_event("startup")  # type: ignore[reportDeprecated]
def startup() -> None:
    """Execute the tasks on app startup."""
    create_postgres_db()


@app.post("/transactions/import")
def import_transactions(
    upload_file: Annotated[UploadFile, File(...)],
    pg_session: Annotated[Session, Depends(get_postgres_session)],
) -> dict[str, int]:
    """Import transactions to the DB from an uploaded file."""
    parser = ParserFactory.create(upload_file=upload_file)

    TransactionService(pg_session=pg_session).import_transactions(parser=parser)

    return {"status": OK}


@app.get("/transactions")
def get_transactions(
    account_id: int,
    from_date: date,
    to_date: date,
    pg_session: Annotated[Session, Depends(get_postgres_session)],
) -> list[Transaction]:
    """Get transactions between provided dates for a provided account."""
    return TransactionService(pg_session=pg_session).get_transactions(
        account_id=account_id,
        from_date=from_date,
        to_date=to_date,
    )


@app.get("/transactions/summary")
def get_transactions_summary(
    account_id: int,
    pg_session: Annotated[Session, Depends(get_postgres_session)],
) -> TransactionsSummary:
    """Get summary of transactions for an account."""
    return TransactionService(pg_session=pg_session).get_transactions_summary(
        account_id
    )
