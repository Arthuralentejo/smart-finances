"""Pydantic schemas for API requests and responses."""

from datetime import date

from pydantic import BaseModel, Field

SUPPORTED_FILE_TYPES = [".pdf", ".csv"]


class TransactionResponse(BaseModel):
    """A single transaction in API responses."""

    date: date
    merchant: str
    description: str
    amount: float
    category: str


class ProcessingResponse(BaseModel):
    """Response from the document processing endpoint."""

    success: bool
    message: str
    transactions: list[TransactionResponse] = Field(default_factory=list)
    transaction_count: int = 0


class ChatRequest(BaseModel):
    """Request body for the chat endpoint."""

    query: str = Field(..., min_length=1, description="Natural language question")


class ChatResponse(BaseModel):
    """Response from the chat endpoint."""

    success: bool
    response: str
    error: str | None = None
