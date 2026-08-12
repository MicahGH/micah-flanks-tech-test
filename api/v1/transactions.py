from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile
from sqlmodel import Session

from cache.summary_cache import SummaryCache, get_summary_cache
from databases.postgres import get_postgres_session
from factories.parser_factory import ParserFactory
from models.dataclasses.import_result import ImportResult
from models.postgres.transaction import Transaction
from models.typed_dicts.transactions_summary import TransactionsSummary
from services.transaction_service import TransactionService

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
)


@router.post("/import")
def import_transactions(
    upload_file: Annotated[UploadFile, File(...)],
    pg_session: Annotated[Session, Depends(get_postgres_session)],
    cache: Annotated[SummaryCache, Depends(get_summary_cache)],
) -> ImportResult:
    """Import transactions to the DB from an uploaded file."""
    parser = ParserFactory.create(upload_file=upload_file)

    return TransactionService(
        pg_session=pg_session,
        cache=cache,
    ).import_transactions(parser=parser)


@router.get("")
def get_transactions(
    account_id: int,
    from_date: date,
    to_date: date,
    pg_session: Annotated[Session, Depends(get_postgres_session)],
    cache: Annotated[SummaryCache, Depends(get_summary_cache)],
) -> list[Transaction]:
    """Get transactions between provided dates for a provided account."""
    return TransactionService(
        pg_session=pg_session,
        cache=cache,
    ).get_transactions(
        account_id=account_id,
        from_date=from_date,
        to_date=to_date,
    )


@router.get("/summary")
def get_transactions_summary(
    account_id: int,
    pg_session: Annotated[Session, Depends(get_postgres_session)],
    cache: Annotated[SummaryCache, Depends(get_summary_cache)],
) -> list[TransactionsSummary]:
    """Get summary of transactions for an account."""
    return TransactionService(
        pg_session=pg_session,
        cache=cache,
    ).get_transactions_summary(account_id)
