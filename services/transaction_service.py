import json
from dataclasses import asdict
from datetime import date
from typing import cast

from pydantic import ValidationError
from sqlmodel import Session

from cache.summary_cache import SummaryCache
from models.dataclasses.import_result import ImportResult
from models.enums.upsert_result import UpsertResult
from models.postgres.malformed_transaction import MalformedTransaction
from models.postgres.transaction import Transaction
from models.pydantic.transaction_import import TransactionImport
from models.typed_dicts.transactions_summary import TransactionsSummary
from parsers.abc_parser import ABCParser
from repositories.malformed_transaction_repository import MalformedTransactionRepository
from repositories.transaction_repository import TransactionRepository
from services.account_service import AccountService


class TransactionService:
    """Service that handles the logic for transactions."""

    def __init__(self, pg_session: Session, cache: SummaryCache) -> None:
        self._session = pg_session
        self._transaction_repo = TransactionRepository(self._session)
        self._account_service = AccountService(self._session)
        self._cache = cache
        self._malformed_transaction_repo = MalformedTransactionRepository(self._session)

    def import_transactions(self, parser: ABCParser) -> ImportResult:
        """Import transactions into the DB."""
        result = ImportResult()

        for raw_transaction in parser.parse():
            result.total += 1

            try:
                transaction_import = TransactionImport.model_validate(
                    asdict(raw_transaction)
                )
            except ValidationError as exc:
                self._malformed_transaction_repo.save(
                    MalformedTransaction(
                        raw_data=asdict(raw_transaction),
                        errors=json.loads(json.dumps(exc.errors(), default=str)),
                    )
                )
                result.malformed += 1
                continue

            account = self._account_service.get_or_create_account(
                external_account_id=transaction_import.account_id,
                entity=transaction_import.entity,
                iban=transaction_import.iban,
            )

            db_transaction = Transaction(
                transaction_id=transaction_import.transaction_id,
                account_id=cast("int", account.id),
                operation_date=transaction_import.operation_date,
                value_date=transaction_import.value_date,
                amount=transaction_import.amount,
                balance=transaction_import.balance,
                currency=transaction_import.currency,
                category=transaction_import.category,
                category_code=transaction_import.category_code,
                transaction_type=transaction_import.transaction_type,
                description=transaction_import.description,
            )

            upsert_result = self._transaction_repo.insert_on_conflict_do_update(
                model=Transaction,
                values=db_transaction.model_dump(exclude={"id"}),
                conflict_columns=["transaction_id"],
            )

            if upsert_result is UpsertResult.INSERTED:
                result.imported += 1
            else:
                result.updated += 1

            self._cache.invalidate(cast("int", account.id))

        self._transaction_repo.commit()
        self._malformed_transaction_repo.commit()

        return result

    def get_transactions(
        self, account_id: int, from_date: date, to_date: date
    ) -> list[Transaction]:
        """Get a list of transactions for the account and dates provided."""
        return self._transaction_repo.get_transactions(account_id, from_date, to_date)

    def get_transactions_summary(self, account_id: int) -> list[TransactionsSummary]:
        """Get a summary of the transactions for the account provided."""
        cached = self._cache.get(account_id)

        if cached:
            return cached

        summary = self._transaction_repo.get_transactions_summary(account_id)

        self._cache.set(
            account_id,
            summary,
        )

        return summary
