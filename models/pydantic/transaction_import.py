import re
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator

from models.enums.category import Category
from models.enums.currency import Currency
from models.enums.entity import Entity

MONTHS_PER_YEAR = 12


class TransactionImport(BaseModel):
    """Validated and normalised transaction imported from the CSV."""

    model_config = ConfigDict(extra="forbid")

    transaction_id: str

    account_id: str
    entity: Entity
    iban: str

    balance: Decimal
    amount: Decimal

    currency: Currency

    category: Category
    category_code: int

    transaction_type: int

    operation_date: date
    value_date: date

    description: str

    @field_validator("*", mode="before")
    @classmethod
    def strip_strings(cls, value: Any) -> Any:  # noqa: ANN401
        """Strip surrounding whitespace from strings."""
        if isinstance(value, str):
            return value.strip()
        return value

    @field_validator("transaction_id", "account_id", "iban")
    @classmethod
    def require_identifier(cls, value: str) -> str:
        """Reject identifiers that are empty after normalisation."""
        if not value:
            msg = "Value is required"
            raise ValueError(msg)
        return value

    @field_validator("entity", mode="before")
    @classmethod
    def normalize_entity(cls, value: object) -> Entity:
        """Normalise and allow only explicitly supported bank entities."""
        return Entity(cls._require_string(value, "Entity").lower())

    @field_validator("category", mode="before")
    @classmethod
    def normalize_category(cls, value: object) -> Category:
        """Normalise category values to the supported taxonomy."""
        return Category.from_raw(cls._require_string(value, "Category"))

    @field_validator("currency", mode="before")
    @classmethod
    def normalize_currency(cls, value: object) -> Currency:
        """Normalize currency."""
        return Currency.from_raw(cls._require_string(value, "Currency"))

    @staticmethod
    def _require_string(value: object, field_name: str) -> str:
        """Return a required string value or a validation-friendly error."""
        if not isinstance(value, str) or not value:
            msg = f"{field_name} must be a non-empty string"
            raise ValueError(msg)
        return value

    @field_validator("category_code", "transaction_type", mode="before")
    @classmethod
    def parse_positive_integer(cls, value: object) -> int:
        """Accept only unambiguous positive integer codes."""
        if isinstance(value, int):
            parsed_value = value
        elif isinstance(value, str) and re.fullmatch(r"[1-9]\d*", value):
            parsed_value = int(value)
        else:
            msg = "Value must be a positive integer"
            raise ValueError(msg)

        if parsed_value <= 0:
            msg = "Value must be a positive integer"
            raise ValueError(msg)

        return parsed_value

    @field_validator("operation_date", "value_date", mode="before")
    @classmethod
    def parse_date(cls, value: object) -> date:
        """Parse an unambiguous date representation."""
        if not isinstance(value, str):
            msg = "Date must be a string"
            raise TypeError(msg)

        normalized = value.strip()
        year_first = re.fullmatch(r"(\d{4})[-/](\d{2})[-/](\d{2})", normalized)
        if year_first:
            year, month, day = (int(part) for part in year_first.groups())
            return cls._build_date(year, month, day)

        day_first = re.fullmatch(r"(\d{2})[-/](\d{2})[-/](\d{4})", normalized)
        if day_first:
            day, month, year = (int(part) for part in day_first.groups())
            if day > MONTHS_PER_YEAR:
                return cls._build_date(year, month, day)

        msg = "Ambiguous or unsupported date format"
        raise ValueError(msg)

    @staticmethod
    def _build_date(year: int, month: int, day: int) -> date:
        """Create a date while converting calendar errors to validation errors."""
        try:
            return date(year, month, day)
        except ValueError as exc:
            msg = "Invalid date"
            raise ValueError(msg) from exc

    @field_validator("amount", "balance", mode="before")
    @classmethod
    def parse_decimal(cls, value: object) -> Decimal:
        """Parse only explicit, unambiguous monetary formats."""
        if isinstance(value, Decimal):
            return value

        if isinstance(value, int) and not isinstance(value, bool):
            return Decimal(value)

        if not isinstance(value, str) or not value.strip():
            msg = "Decimal value is required"
            raise ValueError(msg)

        normalized = cls._normalize_decimal(value)

        try:
            return Decimal(normalized)
        except InvalidOperation as exc:
            msg = "Invalid decimal format"
            raise ValueError(msg) from exc

    @staticmethod
    def _normalize_decimal(value: str) -> str:
        """Normalise a value only when its separators have one meaning."""
        match = re.fullmatch(r"([+-]?)(?:[€$£])?(.+)", value.strip())
        if not match:
            msg = "Invalid decimal format"
            raise ValueError(msg)

        sign, number = match.groups()
        if re.fullmatch(r"\d+|\d+[.]\d{1,2}", number):
            return f"{sign}{number}"

        if re.fullmatch(r"\d+,\d{1,2}", number):
            return f"{sign}{number.replace(',', '.')}"

        if re.fullmatch(r"\d{1,3}(?:,\d{3})+[.]\d{1,2}", number):
            return f"{sign}{number.replace(',', '')}"

        if re.fullmatch(r"\d{1,3}(?:[.]\d{3})+,\d{1,2}", number):
            normalized_number = number.replace(".", "").replace(",", ".")
            return f"{sign}{normalized_number}"

        msg = "Ambiguous or unsupported decimal format"
        raise ValueError(msg)
