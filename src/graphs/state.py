"""State definitions for LangGraph workflows."""

from typing import TypedDict

from src.models import Transaction


class ProcessingState(TypedDict):
    """State for the statement processing workflow."""

    file_path: str
    transactions: list[Transaction]
    status: str
