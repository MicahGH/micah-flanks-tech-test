from decimal import Decimal

from cache.summary_cache import SummaryCache
from models.enums.currency import Currency
from models.typed_dicts.transactions_summary import TransactionsSummary


def test_cache_stores_summary() -> None:
    """Test that a summary is stored in the cache."""
    cache = SummaryCache()

    summary = [
        TransactionsSummary(
            total_balance=Decimal(0),
            total_credits=Decimal(100),
            total_debits=Decimal(-100),
            currency=Currency.EUR,
        )
    ]

    cache.set(
        account_id=1,
        summary=summary,
    )

    result = cache.get(1)

    assert result == summary


def test_cache_returns_none_when_missing() -> None:
    """Test that cache returns none on a cache miss."""
    cache = SummaryCache()

    assert cache.get(999) is None


def test_cache_invalidation() -> None:
    """Test that the cache invalidation functionality works properly."""
    cache = SummaryCache()

    summary = [
        TransactionsSummary(
            total_balance=Decimal(0),
            total_credits=Decimal(100),
            total_debits=Decimal(-100),
            currency=Currency.EUR,
        )
    ]

    cache.set(
        account_id=1,
        summary=summary,
    )

    cache.invalidate(1)

    assert cache.get(1) is None
