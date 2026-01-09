"""LLM client initialization and configuration."""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from src.settings.config import settings

load_dotenv()


def get_llm(temperature: float = 0.0) -> ChatOpenAI:
    """Get a configured LLM instance.

    Args:
        temperature: Model temperature for response randomness.

    Returns:
        Configured ChatOpenAI instance.
    """
    return ChatOpenAI(
        model=settings.llm_model,
        temperature=temperature,
    )
