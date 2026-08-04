from sqlmodel import Session

from models.postgres.account import Account
from repositories.account_repository import AccountRepository


class AccountService:
    """Service that handles the accounts."""

    def __init__(self, pg_session: Session) -> None:
        self._session = pg_session
        self._repository = AccountRepository(self._session)

    def get_or_create_account(
        self,
        external_account_id: str,
        entity: str,
        iban: str,
    ) -> Account:
        """Return an account if it exists, if not, create it and return it."""
        account = self._repository.get_by_external_account_id(external_account_id)

        if account is not None:
            return account

        account = Account(
            external_account_id=external_account_id,
            entity=entity,
            iban=iban,
        )

        self._repository.save(account)
        self._repository.commit()
        self._repository.refresh(account)

        return account
