"""Chat API routes."""

from fastapi import APIRouter, HTTPException

from src.api.schemas import ChatRequest, ChatResponse
from src.graphs import get_analyst_response

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Process a natural language query about transaction data.

    Uses an LLM agent with SQL tools to answer questions about
    the stored transactions.
    """
    try:
        response = get_analyst_response(request.query)
        return ChatResponse(success=True, response=response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
