"""PDF parser that sends the file to a Paddle OCR HTTP service.

This module forwards the PDF to an OCR HTTP service and returns the raw
JSON response. The OCR service URL is provided by the pydantic settings
module at `src.settings.config` (env var `OCR_SERVICE_URL`).
"""

import os
from typing import Any

import httpx

from src.settings.config import settings


async def _call_ocr_service(file_path: str) -> Any:
    """Send the PDF to the OCR service and return the parsed JSON result.

    Args:
        file_path: Path to the PDF file to send.

    Returns:
        Parsed JSON response from the OCR service.

    Raises:
        RuntimeError: if the service responds with an error or invalid JSON.
    """
    async with httpx.AsyncClient() as client:
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f, "application/pdf")}
            try:
                resp = await client.post(settings.ocr_service_url, files=files, timeout=60.0)
            except httpx.RequestError as exc:
                raise RuntimeError(f"Failed to call OCR service: {exc}") from exc

    if resp.status_code < 200 or resp.status_code >= 300:
        raise RuntimeError(f"OCR service returned status {resp.status_code}: {resp.text}")

    try:
        data = resp.json()
    except ValueError as exc:
        raise RuntimeError("OCR service returned non-JSON response") from exc

    # Support responses that wrap result under a key like {'result': [...]}
    if isinstance(data, dict) and "result" in data:
        return data["result"]
    return data


async def load_pdf(file_path: str) -> Any:
    """Send the PDF to the OCR service and return the raw JSON response.

    Args:
        file_path: Path to the PDF file.

    Returns:
        The parsed JSON response from the OCR service (structure depends on
        the OCR implementation).
    """
    return await _call_ocr_service(file_path)
