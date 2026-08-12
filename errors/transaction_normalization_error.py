class TransactionNormalizationError(Exception):
    """Raised when a raw transaction cannot be normalized."""

    def __init__(self, errors: list[dict[str, str]]) -> None:
        self.errors = errors
        super().__init__("Transaction normalization failed")
