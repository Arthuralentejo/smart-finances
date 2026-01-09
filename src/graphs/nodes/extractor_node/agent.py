"""Extractor agent using LangChain's create_agent with ToolStrategy."""

from typing import Callable

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

from src.graphs.nodes.extractor_node.prompts import EXTRACTOR_AGENT_SYSTEM_PROMPT
from src.graphs.nodes.extractor_node.tools import create_extractor_tools
from src.graphs.state import ProcessingState
from src.llm import get_llm
from src.models import TransactionList
from src.parsers.ocr_client import OCRClient


def build_extractor_agent(ocr_client: OCRClient):
    """Create an extractor agent for loading files and extracting transactions.

    Returns:
        A compiled agent graph for extracting transactions from files.
    """
    llm = get_llm()
    tools = create_extractor_tools(ocr_client)

    return create_agent(
        llm,
        tools,
        system_prompt=EXTRACTOR_AGENT_SYSTEM_PROMPT,
        response_format=ToolStrategy(TransactionList),
    )


def build_extractor_node(ocr_client) -> Callable:
    """Create an extractor node function that uses the extractor agent.

    Returns:
        An async function that can be used as a LangGraph node.
    """
    agent = build_extractor_agent(ocr_client)

    async def extractor_node(state: ProcessingState) -> dict:
        """Extract transactions from file using the extractor agent.

        The agent will:
        1. Determine the file type and load the content
        2. Extract all transactions from the content
        3. Return structured transaction data
        """
        file_path = state["file_path"]

        result = await agent.ainvoke(
            {"messages": [("user", f"Extract all transactions from the file at: {file_path}")]}
        )

        structured_response = result.get("structured_response")
        if structured_response is None:
            raise ValueError("Agent did not return structured transaction data")

        return {
            "transactions": structured_response.transactions,
            "status": "extracted",
        }

    return extractor_node
