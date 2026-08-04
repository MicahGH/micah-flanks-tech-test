from enum import StrEnum


class Currency(StrEnum):
    """Supported currencies."""

    EUR = "EUR"
    USD = "USD"
    GBP = "GBP"

    @classmethod
    def from_raw(cls, value: str) -> Currency:
        """Convert raw string to Enum."""
        normalized = value.strip().upper()

        mapping = {
            "€": cls.EUR,
            "EUR": cls.EUR,
            "EURO": cls.EUR,
            "US$": cls.USD,
            "USD": cls.USD,
            "GBP": cls.GBP,
            "£": cls.GBP,
        }

        try:
            return mapping[normalized]
        except KeyError as exc:
            msg = f"Unsupported currency: {value}"
            raise ValueError(msg) from exc
