"""Chat agent for querying transaction data using natural language."""

from langchain.agents import create_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase

from src.database import DATABASE_URL
from src.llm import get_llm

SYSTEM_MESSAGE = """You are a helpful financial analyst assistant. You have access to a
SQLite database containing transaction data with the following schema:

Table: transactions
- id: Primary key
- date: Transaction date
- merchant: Name of the merchant
- description: Transaction description
- amount: Transaction amount (positive for income, negative for expenses)
- category: Transaction category
- source_file: Source file the transaction was extracted from

When answering questions:
1. Use SQL queries to find the relevant data
2. Provide clear, concise answers
3. Format monetary values appropriately
4. If asked about spending or expenses, focus on the amounts and categories
5. Be helpful and informative about the user's financial data
"""


def get_analyst_response(query: str) -> str:
    """Process a natural language query about transactions and return a response.

    Args:
        query: Natural language question about the transaction data.

    Returns:
        A string response answering the user's question.
    """
    db = SQLDatabase.from_uri(DATABASE_URL)

    llm = get_llm(temperature=0)

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    agent = create_agent(
        llm,
        toolkit.get_tools(),
        system_prompt=SYSTEM_MESSAGE,
    )

    result = agent.invoke({"messages": [("user", query)]})

    final_message = result["messages"][-1]
    return final_message.content
