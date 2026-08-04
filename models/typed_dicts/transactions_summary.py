from decimal import Decimal
from typing import TypedDict


class TransactionsSummary(TypedDict):
    """Summary of transactions."""

    total_balance: Decimal
    total_credits: Decimal
    total_debits: Decimal
