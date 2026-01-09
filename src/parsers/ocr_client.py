from typing import Any

import httpx


class OCRClient:
    """Encapsulates calls to the remote Paddle OCR HTTP API."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client

    async def aclose(self) -> None:
        """Close the underlying HTTP client."""
        await self.client.aclose()

    async def send_pdf(self, file_path: str) -> Any:
        """POST a PDF file to the OCR service and return parsed JSON.

        Raises RuntimeError on transport errors, non-2xx responses, or
        non-JSON responses.
        """
        with open(file_path, "rb") as f:
            files = {"file": (file_path.split("/")[-1], f, "application/pdf")}
            try:
                resp = await self.client.post("/ocr", files=files)
                resp.raise_for_status()
            except httpx.RequestError as exc:
                raise RuntimeError(f"Failed to call OCR service: {exc}") from exc
        try:
            data = resp.json()
        except ValueError as exc:
            raise RuntimeError("OCR service returned non-JSON response") from exc

        if isinstance(data, dict) and "texts" in data:
            return data["texts"]
        return data
