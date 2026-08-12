from models.dataclasses.raw_transaction import RawTransaction


def create_raw_transaction(
    transaction_id: str = "tx-001",
) -> RawTransaction:
    """Helper function to create a raw transaction."""
    return RawTransaction(
        transaction_id=transaction_id,
        account_id="external-account-1",
        entity="santander",
        iban="ES123456789",
        balance="1000.00",
        amount="-100.00",
        currency="EUR",
        category="TRANSPORTE",
        category_code="102",
        transaction_type="126",
        operation_date="2024-01-01",
        value_date="2024-01-02",
        description="METRO",
    )
