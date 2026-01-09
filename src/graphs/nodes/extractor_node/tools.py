"""Tools for the extractor agent."""

import asyncio
import concurrent.futures
from typing import Any

import pandas as pd
from langchain_core.tools import tool

from src.parsers.ocr_client import OCRClient


def create_extractor_tools(ocr_client: OCRClient) -> list:
    """Create tools for loading files.

    Returns:
        List of tools for the extractor agent.
    """

    @tool
    def load_csv_file(file_path: str) -> str:
        """Load a CSV file and return its contents as a Markdown table.

        Args:
            file_path: Path to the CSV file.

        Returns:
            CSV contents formatted as a Markdown table.
        """
        df = pd.read_csv(file_path)
        return df.to_markdown(index=False)

    @tool
    def load_pdf_file(file_path: str) -> Any:
        """Load a PDF bank statement file and extract its content using OCR.

        Use this tool when the file has a .pdf extension.

        Args:
            file_path: The path to the PDF file to load.

        Returns:
            The extracted text content from the PDF.
        """
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop is not None:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, ocr_client.send_pdf(file_path))
                return future.result()
        else:
            return asyncio.run(ocr_client.send_pdf(file_path))

    return [load_csv_file, load_pdf_file]
