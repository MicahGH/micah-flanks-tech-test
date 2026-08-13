from unittest.mock import Mock

from models.postgres.account import Account
from services.account_service import AccountService


def test_get_or_create_account_creates_new_account() -> None:
    """Test that get_or_create_account() creates an account if it doesn't exist."""
    repository = Mock()

    repository.get_by_external_account_id.return_value = None

    service = AccountService.__new__(AccountService)
    object.__setattr__(service, "_repository", repository)

    result = service.get_or_create_account(
        external_account_id="acc-123",
        entity="santander",
        iban="ES123",
    )

    assert result.external_account_id == "acc-123"
    assert result.entity == "santander"
    assert result.iban == "ES123"

    repository.save.assert_called_once_with(result)
    repository.commit.assert_called_once()
    repository.refresh.assert_called_once_with(result)


def test_get_or_create_account_returns_existing_account() -> None:
    """Test that get_or_create_account() returns an account if it already exists."""
    repository = Mock()

    existing_account = Account(
        id=1,
        external_account_id="acc-123",
        entity="santander",
        iban="ES123",
    )

    repository.get_by_external_account_id.return_value = existing_account

    service = AccountService.__new__(AccountService)
    object.__setattr__(service, "_repository", repository)

    result = service.get_or_create_account(
        external_account_id="acc-123",
        entity="santander",
        iban="ES123",
    )

    assert result == existing_account

    repository.get_by_external_account_id.assert_called_once_with("acc-123")

    repository.save.assert_not_called()
    repository.commit.assert_not_called()
    repository.refresh.assert_not_called()
