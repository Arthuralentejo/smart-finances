"""LLM client initialization and configuration."""

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def get_llm(temperature: float = 0.0) -> ChatOpenAI:
    """Get a configured LLM instance.

    Args:
        temperature: Model temperature for response randomness.

    Returns:
        Configured ChatOpenAI instance.
    """
    return ChatOpenAI(
        model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
        temperature=temperature,
    )
