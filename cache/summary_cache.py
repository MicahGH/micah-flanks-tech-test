from cachetools import TTLCache

from models.typed_dicts.transactions_summary import TransactionsSummary


class SummaryCache:
    """In-memory cache for transaction summaries."""

    def __init__(
        self,
        max_size: int = 1000,
        ttl_seconds: int = 300,
    ) -> None:
        self._cache = TTLCache(
            maxsize=max_size,
            ttl=ttl_seconds,
        )

    def get(self, account_id: int) -> list[TransactionsSummary] | None:
        """Get a value from the cache."""
        return self._cache.get(account_id)

    def set(
        self,
        account_id: int,
        summary: list[TransactionsSummary],
    ) -> None:
        """Set a k-v in the cache."""
        self._cache[account_id] = summary

    def invalidate(self, account_id: int) -> None:
        """Invalidate a k-v in the cache."""
        self._cache.pop(account_id, None)

    def clear(self) -> None:
        """Clear the entire cache."""
        self._cache.clear()
