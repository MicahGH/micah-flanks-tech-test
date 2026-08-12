from decimal import Decimal
from typing import TypedDict

from models.enums.currency import Currency


class TransactionsSummary(TypedDict):
    """Summary of transactions."""

    total_balance: Decimal
    total_credits: Decimal
    total_debits: Decimal
    currency: Currency
