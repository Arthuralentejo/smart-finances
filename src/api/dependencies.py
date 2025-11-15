"""FastAPI dependencies for dependency injection."""

from typing import Annotated

from fastapi import Depends, Request
from langgraph.graph.state import CompiledStateGraph


def get_processing_graph(request: Request) -> CompiledStateGraph:
    """Get the processing graph from app state.

    Args:
        request: FastAPI request object containing app state.

    Returns:
        The compiled processing graph.
    """
    return request.state.processing_graph


ProcessingGraphDep = Annotated[CompiledStateGraph, Depends(get_processing_graph)]
