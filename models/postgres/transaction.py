from typing import TYPE_CHECKING

from sqlmodel.main import Field, SQLModel

if TYPE_CHECKING:
    from datetime import date
    from decimal import Decimal


class Transaction(SQLModel, table=True):
    """SQL model for the 'transaction' table."""

    __tablename__ = "transaction"  # type: ignore[reportAssignmentType]

    id: int | None = Field(default=None, primary_key=True)

    transaction_id: str = Field(unique=True, index=True)

    account_id: int = Field(foreign_key="account.id", index=True)

    operation_date: date
    value_date: date

    amount: Decimal
    balance: Decimal

    currency: str

    category: str
    category_code: int

    transaction_type: int

    description: str
