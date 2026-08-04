from typing import TYPE_CHECKING

from sqlmodel import col, func, select

from models.postgres.transaction import Transaction
from models.typed_dicts.transactions_summary import TransactionsSummary
from repositories.base_repository import BaseRepository

if TYPE_CHECKING:
    from datetime import date


class TransactionRepository(BaseRepository[Transaction]):
    """Repository for the transaction table."""

    def get_transactions(
        self, account_id: int, from_date: date, to_date: date
    ) -> list[Transaction]:
        """Get transactions between provided dates."""
        statement = select(Transaction).where(
            col(Transaction.operation_date).between(from_date, to_date)
            and col(Transaction.account_id) == account_id
        )
        return list(self._session.exec(statement).all())

    def get_transactions_summary(self, account_id: int) -> TransactionsSummary:
        """Get a summary of the transactions for the provided account."""
        statement = select(
            func.coalesce(func.sum(Transaction.amount), 0).label("total_balance"),
            func.coalesce(
                func.sum(Transaction.amount).filter(col(Transaction.amount) > 0),
                0,
            ).label("total_credits"),
            func.coalesce(
                func.sum(Transaction.amount).filter(col(Transaction.amount) < 0),
                0,
            ).label("total_debits"),
        ).where(Transaction.account_id == account_id)

        result = self._session.execute(statement).mappings().one()  # type: ignore[reportDeprecated]
        return TransactionsSummary(**result)
