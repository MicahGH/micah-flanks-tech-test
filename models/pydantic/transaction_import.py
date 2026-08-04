from typing import TYPE_CHECKING

from dateutil.parser import parse
from pydantic import BaseModel, field_validator

from models.enums.category import Category
from models.enums.currency import Currency
from models.enums.entity import Entity

if TYPE_CHECKING:
    from datetime import date
    from decimal import Decimal


class TransactionImport(BaseModel):
    """Validated and normalised transaction imported from the CSV."""

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
    def strip_strings(cls, value: str) -> str:
        """Strip whitespace inside strings."""
        return value.strip()

    @field_validator("entity", mode="before")
    @classmethod
    def normalize_entity(cls, value: str) -> Entity:
        """Normalize entity column."""
        return Entity(value.strip().lower())

    @field_validator("currency", mode="before")
    @classmethod
    def normalize_currency(cls, value: str) -> Currency:
        """Normalize currency column."""
        return Currency.from_raw(value)

    @field_validator("category", mode="before")
    @classmethod
    def normalize_category(cls, value: str) -> Category:
        """Normalize category column."""
        return Category.from_raw(value)

    @field_validator("operation_date", "value_date", mode="before")
    @classmethod
    def parse_date(cls, value: str) -> date:
        """Parse the date column to be standard."""
        return parse(value, dayfirst=True).date()
