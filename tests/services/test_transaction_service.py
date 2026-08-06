from unittest.mock import Mock

from services.transaction_service import TransactionService
from tests.helpers import create_raw_transaction


def test_duplicate_transaction_is_ignored(
    transaction_service: TransactionService,
) -> None:
    """Test that duplicate transactions are ignored in the transaction service."""
    parser = Mock()

    parser.parse.return_value = [create_raw_transaction(transaction_id="same-id")]

    first = transaction_service.import_transactions(parser)

    second = transaction_service.import_transactions(parser)

    assert first.imported == 1
    assert first.duplicates == 0

    assert second.imported == 0
    assert second.duplicates == 1
