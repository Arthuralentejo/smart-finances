from datetime import date

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from src.database import TransactionModel, init_db, save_transactions


def test_save_transaction():
    """Test that we can initialize the DB and save a transaction."""
    engine = create_engine("sqlite:///:memory:")
    init_db(engine)

    transactions = [
        {
            "transaction_date": date(2024, 1, 15),
            "merchant": "Grocery Store",
            "description": "Weekly groceries",
            "amount": -85.50,
            "category": "Food",
            "source_file": "statement_jan.pdf",
        }
    ]

    save_transactions(transactions, engine)

    with Session(engine) as session:
        result = session.execute(select(TransactionModel)).scalar_one()
        assert result.merchant == "Grocery Store"
        assert result.amount == -85.50
        assert result.transaction_date == date(2024, 1, 15)
