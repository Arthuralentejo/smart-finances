from datetime import date

from sqlalchemy import Date, Float, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

DATABASE_URL = "sqlite:///data/database/pfm.db"

engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase):
    pass


class TransactionModel(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    transaction_date: Mapped[date] = mapped_column(Date)
    merchant: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    amount: Mapped[float] = mapped_column(Float)
    category: Mapped[str] = mapped_column(String)
    source_file: Mapped[str] = mapped_column(String)


def init_db(db_engine=None) -> None:
    """Initialize the database by creating all tables."""
    target_engine = db_engine or engine
    Base.metadata.create_all(target_engine)


def save_transactions(transactions: list[dict], db_engine=None) -> None:
    """Save a list of transaction dictionaries to the database."""
    target_engine = db_engine or engine
    with Session(target_engine) as session:
        for txn in transactions:
            model = TransactionModel(**txn)
            session.add(model)
        session.commit()
