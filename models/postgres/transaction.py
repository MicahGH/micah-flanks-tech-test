from datetime import date  # noqa: TC003
from decimal import Decimal  # noqa: TC003

from sqlmodel import Index
from sqlmodel.main import Field, SQLModel


class Transaction(SQLModel, table=True):
    """SQL model for the 'transaction' table."""

    __tablename__ = "transaction"  # type: ignore[reportAssignmentType]

    __table_args__ = (
        Index(
            "cix_transactions_account_date",
            "account_id",
            "operation_date",
        ),
    )

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
