"""LangGraph workflow builder for processing bank statements."""

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from src.graphs.nodes import extractor_node, loader_node, saver_node
from src.graphs.state import ProcessingState


def build_processing_graph() -> CompiledStateGraph:
    """Build and compile the statement processing graph.

    Returns:
        Compiled LangGraph ready for invocation.
    """
    graph_builder = StateGraph(ProcessingState)

    graph_builder.add_node("loader_node", loader_node)
    graph_builder.add_node("extractor_node", extractor_node)
    graph_builder.add_node("saver_node", saver_node)

    graph_builder.add_edge(START, "loader_node")
    graph_builder.add_edge("loader_node", "extractor_node")
    graph_builder.add_edge("extractor_node", "saver_node")
    graph_builder.add_edge("saver_node", END)

    return graph_builder.compile()
