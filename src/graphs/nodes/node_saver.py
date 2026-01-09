"""Saver node for persisting transactions to the database."""

from src.database import init_db, save_transactions
from src.graphs.state import ProcessingState


def saver_node(state: ProcessingState) -> dict:
    """Save transactions to the database."""
    init_db()
    transaction_dicts = []
    for txn in state["transactions"]:
        data = txn.model_dump()
        data["source_file"] = state["file_path"]
        transaction_dicts.append(data)
    save_transactions(transaction_dicts)
    return {"status": "saved"}
