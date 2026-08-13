from cachetools import TTLCache
from fastapi import Request

from models.typed_dicts.transactions_summary import TransactionsSummary


def get_summary_cache(request: Request) -> SummaryCache:
    """Get the summary cache from the app's state."""
    return request.app.state.summary_cache


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

    def get(self, external_account_id: str) -> list[TransactionsSummary] | None:
        """Get a value from the cache."""
        return self._cache.get(external_account_id)

    def set(
        self,
        external_account_id: str,
        summary: list[TransactionsSummary],
    ) -> None:
        """Set a k-v in the cache."""
        self._cache[external_account_id] = summary

    def invalidate(self, external_account_id: str) -> None:
        """Invalidate a k-v in the cache."""
        self._cache.pop(external_account_id, None)

    def clear(self) -> None:
        """Clear the entire cache."""
        self._cache.clear()
