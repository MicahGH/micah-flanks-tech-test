from unittest.mock import Mock

from services.transaction_service import TransactionService
from tests.helpers import create_raw_transaction


def test_transaction_is_updated(
    transaction_service: TransactionService,
) -> None:
    """Test that transactions are updated in the transaction service if existing."""
    parser = Mock()

    parser.parse.return_value = [create_raw_transaction(transaction_id="same-id")]

    first = transaction_service.import_transactions(parser)

    second = transaction_service.import_transactions(parser)

    assert first.imported == 1
    assert first.updated == 0

    assert second.imported == 0
    assert second.updated == 1
