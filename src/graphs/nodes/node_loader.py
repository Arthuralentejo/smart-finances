"""Loader node for reading and parsing files."""

from pathlib import Path

from src.graphs.state import ProcessingState
from src.parsers import load_csv, load_pdf


def loader_node(state: ProcessingState) -> dict:
    """Read file and extract raw text.

    Supports CSV and PDF file formats.
    """
    file_path = state["file_path"]
    extension = Path(file_path).suffix.lower()

    if extension == ".csv":
        raw_text = load_csv(file_path)
    elif extension == ".pdf":
        raw_text = load_pdf(file_path)
    else:
        raise ValueError(f"Unsupported file format: {extension}")

    return {"raw_text": raw_text, "status": "loaded"}
