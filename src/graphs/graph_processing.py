"""LangGraph workflow builder for processing bank statements."""

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from src.graphs.nodes import (
    build_categorizer_node,
    build_extractor_node,
    saver_node,
)
from src.graphs.state import ProcessingState


def build_processing_graph(ocr_client) -> CompiledStateGraph:
    """Build and compile the statement processing graph.

    The graph has three nodes:
    1. extractor_node: An agent that loads files and extracts transactions
    2. categorizer_node: An agent that categorizes transactions using web search
    3. saver_node: Saves extracted transactions to the database

    Args:
        ocr_client: The OCR client for PDF processing.

    Returns:
        Compiled LangGraph ready for invocation.
    """
    extractor_node = build_extractor_node(ocr_client)
    categorizer_node = build_categorizer_node()

    graph_builder = StateGraph(ProcessingState)

    graph_builder.add_node("extractor_node", extractor_node)
    graph_builder.add_node("categorizer_node", categorizer_node)
    graph_builder.add_node("saver_node", saver_node)

    graph_builder.add_edge(START, "extractor_node")
    graph_builder.add_edge("extractor_node", "categorizer_node")
    graph_builder.add_edge("categorizer_node", "saver_node")
    graph_builder.add_edge("saver_node", END)

    return graph_builder.compile()
