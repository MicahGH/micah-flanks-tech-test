from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RawTransaction:
    """Raw transaction as received from the CSV."""

    transaction_id: str
    account_id: str
    entity: str
    iban: str
    balance: str
    amount: str
    currency: str
    category: str
    category_code: str
    transaction_type: str
    operation_date: str
    value_date: str
    description: str
