from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from decimal import Decimal


class TransactionsSummary(TypedDict):
    """Summary of transactions."""

    total_balance: Decimal
    total_credits: Decimal
    total_debits: Decimal
