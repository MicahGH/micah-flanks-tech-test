from datetime import date
from decimal import Decimal

import pytest
from pydantic import ValidationError

from models.pydantic.transaction_import import TransactionImport


def test_transaction_import_normalizes_decimal() -> None:
    """Test that the transaction import normalizes decimals properly."""
    transaction = TransactionImport.model_validate(
        {
            "transaction_id": "tx-1",
            "account_id": "account-1",
            "entity": "santander",
            "iban": "ES123",
            "balance": "21,002.94",
            "amount": "-€1,234.50",
            "currency": "€",
            "category": "TRANSPORTE",
            "category_code": "102",
            "transaction_type": "126",
            "operation_date": "2024-01-01",
            "value_date": "2024-01-02",
            "description": "METRO",
        }
    )

    assert transaction.balance == Decimal("21002.94")
    assert transaction.amount == Decimal("-1234.50")


def test_transaction_import_parses_dates() -> None:
    """Test that the transaction import parses dates properly."""
    transaction = TransactionImport.model_validate(
        {
            "transaction_id": "tx-2",
            "account_id": "account-1",
            "entity": "santander",
            "iban": "ES123",
            "balance": "100",
            "amount": "10",
            "currency": "EUR",
            "category": "SALUD",
            "category_code": "1",
            "transaction_type": "1",
            "operation_date": "23-12-2024",
            "value_date": "24/12/2024",
            "description": "TEST",
        }
    )

    assert transaction.operation_date == date(2024, 12, 23)
    assert transaction.value_date == date(2024, 12, 24)


def test_invalid_transaction_is_rejected() -> None:
    """Test that the transaction import rejects a malformed transaction."""
    with pytest.raises(ValidationError):
        TransactionImport.model_validate(
            {
                "transaction_id": "tx",
                "amount": "not-a-number",
            }
        )
