from datetime import date

from sqlmodel import and_, col, func, select

from models.postgres.account import Account
from models.postgres.transaction import Transaction
from models.typed_dicts.transactions_summary import TransactionsSummary
from repositories.base_repository import BaseRepository


class TransactionRepository(BaseRepository[Transaction]):
    """Repository for the transaction table."""

    def get_transactions(
        self, external_account_id: str, from_date: date, to_date: date
    ) -> list[Transaction]:
        """Get transactions between provided dates."""
        statement = (
            select(Transaction)
            .join(Account, col(Account.external_account_id) == external_account_id)
            .where(
                and_(
                    col(Transaction.operation_date).between(from_date, to_date),
                )
            )
        )
        return list(self._session.exec(statement).all())

    def get_transactions_summary(
        self, external_account_id: str
    ) -> list[TransactionsSummary]:
        """Get a summary of the transactions for the provided account."""
        statement = (
            select(
                func.coalesce(func.sum(Transaction.amount), 0).label("total_balance"),
                func.coalesce(
                    func.sum(Transaction.amount).filter(col(Transaction.amount) > 0),
                    0,
                ).label("total_credits"),
                func.coalesce(
                    func.sum(Transaction.amount).filter(col(Transaction.amount) < 0),
                    0,
                ).label("total_debits"),
                Transaction.currency,
            )
            .join(Account, col(Account.external_account_id) == external_account_id)
            .group_by(col(Transaction.currency), col(Transaction.account_id))
        )

        result = self._session.execute(statement).mappings()  # type: ignore[reportDeprecated]

        return [TransactionsSummary(**row) for row in result]
