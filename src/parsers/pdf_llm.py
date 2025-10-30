"""LLM-based PDF parser using vision capabilities."""

import base64
import io

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pdf2image import convert_from_path
from src.llm.client import get_llm

EXTRACTION_SYSTEM_PROMPT = """You are a financial document extraction specialist. Your task is to extract
all text content from bank statement images, preserving the structure and layout as much as possible.

Focus on extracting:
1. Transaction dates
2. Merchant/payee names
3. Transaction descriptions
4. Amounts (both debits and credits)
5. Running balances (if present)
6. Account information headers

Format the extracted content as a structured table with columns separated by tabs.
Each transaction should be on its own line.
Preserve the original order of transactions as they appear in the document.

If you see a table structure, maintain the column alignment using tabs.
For headers and metadata, include them at the top of the output.

Be thorough and extract ALL visible text related to transactions."""

PAGE_EXTRACTION_PROMPT = """Extract all financial transaction data from this bank statement page.

Provide the output as tab-separated values preserving the table structure.
Include all dates, descriptions, merchants, and amounts you can identify.

If this appears to be a continuation of a previous page, just extract the transactions
without repeating headers unless new headers are visible."""


def _encode_image_to_base64(image) -> str:
    """Convert a PIL Image to base64 string."""
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def _pdf_to_images(file_path: str, dpi: int = 150) -> list:
    """Convert PDF pages to PIL Images.

    Args:
        file_path: Path to the PDF file.
        dpi: Resolution for rendering (higher = better quality but slower).

    Returns:
        List of PIL Image objects, one per page.
    """
    return convert_from_path(file_path, dpi=dpi)


def _extract_page_with_llm(llm: ChatOpenAI, image, page_num: int) -> str:
    """Extract text from a single page image using LLM vision.

    Args:
        llm: The LLM client with vision capabilities.
        image: PIL Image of the page.
        page_num: Page number for context.

    Returns:
        Extracted text content from the page.
    """
    base64_image = _encode_image_to_base64(image)

    messages = [
        SystemMessage(content=EXTRACTION_SYSTEM_PROMPT),
        HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": f"Page {page_num}: {PAGE_EXTRACTION_PROMPT}",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}",
                        "detail": "high",
                    },
                },
            ]
        ),
    ]

    response = llm.invoke(messages)
    return response.content


def load_pdf_with_llm(file_path: str, model: str | None = None) -> str:
    """Extract text from a PDF using LLM vision capabilities.

    This parser converts PDF pages to images and uses a vision-capable LLM
    to extract and structure the text content. It's particularly effective
    for complex layouts and scanned documents.

    Args:
        file_path: Path to the PDF file.
        model: Optional model override (must support vision, e.g., 'gpt-4o').

    Returns:
        Extracted and structured text from all pages.
    """
    # Use a vision-capable model
    llm = get_llm()

    # Convert PDF to images
    images = _pdf_to_images(file_path)

    # Extract text from each page
    all_pages_text = []
    for page_num, image in enumerate(images, start=1):
        page_text = _extract_page_with_llm(llm, image, page_num)
        all_pages_text.append(f"--- Page {page_num} ---\n{page_text}")

    return "\n\n".join(all_pages_text)
