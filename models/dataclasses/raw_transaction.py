from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RawTransaction:
    """Raw transaction as received from the CSV."""

    transaction_id: str | None
    account_id: str | None
    entity: str | None
    iban: str | None
    balance: str | None
    amount: str | None
    currency: str | None
    category: str | None
    category_code: str | None
    transaction_type: str | None
    operation_date: str | None
    value_date: str | None
    description: str | None
