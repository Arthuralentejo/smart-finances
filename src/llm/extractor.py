"""LLM-based transaction extraction from bank statement text."""

from langchain_core.prompts import ChatPromptTemplate

from src.llm.client import get_llm
from src.models import Transaction, TransactionList

EXTRACTION_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a financial data extraction assistant. Extract all transactions "
        "from bank statements accurately. For each transaction, identify the date, "
        "merchant, description, amount (negative for expenses, positive for income), "
        "and categorize it appropriately.",
    ),
    (
        "human",
        """Extract all financial transactions from the following bank statement text.

Bank statement text:
{raw_text}

Extract all transactions.""",
    ),
])


def extract_transactions(raw_text: str) -> list[Transaction]:
    """Use an LLM to extract and normalize transactions from raw text.

    Args:
        raw_text: Raw text extracted from a bank statement.

    Returns:
        List of Transaction objects with categorized expenses.
    """
    llm = get_llm(temperature=0.0)

    # Use with_structured_output with a proper Pydantic model
    structured_llm = llm.with_structured_output(TransactionList)

    chain = EXTRACTION_PROMPT | structured_llm
    result = chain.invoke({"raw_text": raw_text})
    return result.transactions
