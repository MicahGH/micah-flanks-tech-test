from datetime import date
from typing import cast

from sqlmodel import Session

from models.postgres.transaction import Transaction
from models.pydantic.transaction_import import TransactionImport
from models.typed_dicts.transactions_summary import TransactionsSummary
from parsers.abc_parser import ABCParser
from repositories.transaction_repository import TransactionRepository
from services.account_service import AccountService


class TransactionService:
    """Service that handles the transactions provided."""

    def __init__(self, pg_session: Session) -> None:
        self._session = pg_session
        self._repository = TransactionRepository(self._session)
        self._account_service = AccountService(self._session)

    def import_transactions(self, parser: ABCParser) -> None:
        """Import transactions into the DB."""
        for row in parser.parse():
            transaction = TransactionImport.model_validate(row)

            account = self._account_service.get_or_create_account(
                external_account_id=transaction.account_id,
                entity=transaction.entity,
                iban=transaction.iban,
            )

            db_transaction = Transaction(
                transaction_id=transaction.transaction_id,
                account_id=cast("int", account.id),
                operation_date=transaction.operation_date,
                value_date=transaction.value_date,
                amount=transaction.amount,
                balance=transaction.balance,
                currency=transaction.currency,
                category=transaction.category,
                category_code=transaction.category_code,
                transaction_type=transaction.transaction_type,
                description=transaction.description,
            )

            self._repository.save(db_transaction)

        self._repository.commit()

    def get_transactions(
        self, account_id: int, from_date: date, to_date: date
    ) -> list[Transaction]:
        """Get a list of transactions for the account and dates provided."""
        return self._repository.get_transactions(account_id, from_date, to_date)

    def get_transactions_summary(self, account_id: int) -> TransactionsSummary:
        """Get a summary of the transactions for the account provided."""
        return self._repository.get_transactions_summary(account_id)
