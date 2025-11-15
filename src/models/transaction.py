"""Pydantic models for financial transactions."""

from datetime import date

from pydantic import BaseModel, Field


class Transaction(BaseModel):
    """A single financial transaction."""

    transaction_date: date
    merchant: str
    description: str
    amount: float = Field(description="Negative for expenses, positive for income")
    category: str = Field(
        description="One of: Food, Transport, Shopping, Entertainment, Bills, Health, Income, Transfer, Other"
    )
    source_file: str = Field(default="uploaded")


class TransactionList(BaseModel):
    """A list of extracted transactions from a bank statement."""

    transactions: list[Transaction] = Field(
        description="List of all transactions extracted from the statement"
    )
