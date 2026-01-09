"""Categorizer agent using LangChain's create_agent with ToolStrategy."""

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

from src.graphs.nodes.categorizer_node.prompts import CATEGORIZER_AGENT_SYSTEM_PROMPT
from src.graphs.nodes.categorizer_node.tools import create_categorizer_tools
from src.graphs.state import ProcessingState
from src.llm import get_llm
from src.models import Transaction, TransactionList


def build_categorizer_agent():
    """Create a categorizer agent for improving transaction categories.

    Returns:
        A compiled agent graph for categorizing transactions.
    """
    llm = get_llm()
    tools = create_categorizer_tools()

    return create_agent(
        llm,
        tools,
        system_prompt=CATEGORIZER_AGENT_SYSTEM_PROMPT,
        response_format=ToolStrategy(TransactionList),
    )


def build_categorizer_node():
    """Create a categorizer node function that uses the categorizer agent.

    Returns:
        An async function that can be used as a LangGraph node.
    """
    agent = build_categorizer_agent()

    async def categorizer_node(state: ProcessingState) -> dict:
        """Categorize transactions using the categorizer agent.

        The agent will:
        1. Review each transaction's category
        2. Search for company information when needed
        3. Return updated transactions with improved categories
        """
        transactions = state["transactions"]

        transaction_text = "\n".join(
            f"- {t.transaction_date}: {t.merchant} - {t.description} "
            f"(${t.amount:.2f}) [Current category: {t.category}]"
            for t in transactions
        )

        result = await agent.ainvoke(
            {
                "messages": [
                    ("user", f"Review and categorize these transactions:\n\n{transaction_text}")
                ]
            }
        )

        structured_response = result.get("structured_response")
        if structured_response is None:
            return {"status": "categorized"}

        categorized_transactions = []
        for i, txn in enumerate(structured_response.transactions):
            source_file = transactions[i].source_file if i < len(transactions) else "uploaded"
            categorized_transactions.append(
                Transaction(
                    transaction_date=txn.transaction_date,
                    merchant=txn.merchant,
                    description=txn.description,
                    amount=txn.amount,
                    category=txn.category,
                    source_file=source_file,
                )
            )

        return {
            "transactions": categorized_transactions,
            "status": "categorized",
        }

    return categorizer_node
