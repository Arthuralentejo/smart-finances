"""Extractor node for LLM-based transaction extraction."""

from src.graphs.state import ProcessingState
from src.llm import extract_transactions


def extractor_node(state: ProcessingState) -> dict:
    """Extract transactions from raw text using LLM."""
    transactions = extract_transactions(state["raw_text"])
    return {"transactions": transactions, "status": "extracted"}
