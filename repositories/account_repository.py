from sqlmodel import select

from models.postgres.account import Account
from repositories.base_repository import BaseRepository


class AccountRepository(BaseRepository[Account]):
    """Repository for the account table."""

    def get_by_external_account_id(
        self,
        external_account_id: str,
    ) -> Account | None:
        """Get an account from the DB using its external account ID or return none."""
        statement = select(Account).where(
            Account.external_account_id == external_account_id
        )

        return self._session.exec(statement).first()
