"""Tests for file parsers."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.parsers import load_csv, load_pdf_with_llm
from src.parsers.pdf_llm import _encode_image_to_base64


def test_load_csv_file():
    """Test that load_csv correctly loads a CSV and converts to markdown."""
    csv_content = """date,description,amount
2024-01-15,Grocery Store,-85.50
2024-01-16,Gas Station,-45.00
2024-01-17,Salary,3000.00"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(csv_content)
        temp_path = f.name

    try:
        result = load_csv(temp_path)

        assert "date" in result
        assert "description" in result
        assert "amount" in result
        assert "Grocery Store" in result
        assert "-85.5" in result or "-85.50" in result
    finally:
        Path(temp_path).unlink()


def test_encode_image_to_base64():
    """Test that image encoding to base64 works correctly."""
    from PIL import Image

    # Create a simple test image
    image = Image.new("RGB", (100, 100), color="white")

    result = _encode_image_to_base64(image)

    # Should return a non-empty base64 string
    assert isinstance(result, str)
    assert len(result) > 0
    # Base64 strings only contain these characters
    import base64

    try:
        base64.b64decode(result)
    except Exception:
        assert False, "Result is not valid base64"


def test_load_pdf_with_llm_mocked():
    """Test LLM-based PDF loading with mocked dependencies."""
    from PIL import Image

    # Create a mock image
    mock_image = Image.new("RGB", (100, 100), color="white")

    # Mock LLM response
    mock_llm_response = MagicMock()
    mock_llm_response.content = "Date\tDescription\tAmount\n2024-01-15\tGrocery Store\t-85.50"

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        temp_path = f.name

    try:
        with (
            patch("src.parsers.pdf_llm._pdf_to_images") as mock_pdf_to_images,
            patch("src.parsers.pdf_llm.get_llm") as mock_get_llm,
        ):
            mock_pdf_to_images.return_value = [mock_image]
            mock_llm = MagicMock()
            mock_llm.invoke.return_value = mock_llm_response
            mock_get_llm.return_value = mock_llm

            result = load_pdf_with_llm(temp_path)

            assert "Page 1" in result
            assert "Date" in result
            assert "Grocery Store" in result
            assert "-85.50" in result

            # Verify LLM was called
            mock_llm.invoke.assert_called_once()
    finally:
        Path(temp_path).unlink()


def test_load_pdf_with_llm_multiple_pages_mocked():
    """Test LLM-based PDF loading with multiple pages."""
    from PIL import Image

    # Create mock images for two pages
    mock_images = [
        Image.new("RGB", (100, 100), color="white"),
        Image.new("RGB", (100, 100), color="gray"),
    ]

    # Mock LLM responses for each page
    page1_response = MagicMock()
    page1_response.content = "Page 1 content: Transaction A"

    page2_response = MagicMock()
    page2_response.content = "Page 2 content: Transaction B"

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        temp_path = f.name

    try:
        with (
            patch("src.parsers.pdf_llm._pdf_to_images") as mock_pdf_to_images,
            patch("src.parsers.pdf_llm.get_llm") as mock_get_llm,
        ):
            mock_pdf_to_images.return_value = mock_images
            mock_llm = MagicMock()
            mock_llm.invoke.side_effect = [page1_response, page2_response]
            mock_get_llm.return_value = mock_llm

            result = load_pdf_with_llm(temp_path)

            assert "Page 1" in result
            assert "Page 2" in result
            assert "Transaction A" in result
            assert "Transaction B" in result

            # Verify LLM was called twice (once per page)
            assert mock_llm.invoke.call_count == 2
    finally:
        Path(temp_path).unlink()
