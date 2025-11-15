"""Tests for file parsers."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.parsers import load_csv, load_pdf, load_pdf_with_llm
from src.parsers.pdf import _reconstruct_layout
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


def test_reconstruct_layout_empty():
    """Test that _reconstruct_layout handles empty input."""
    assert _reconstruct_layout([]) == ""
    assert _reconstruct_layout([None]) == ""
    assert _reconstruct_layout([[None]]) == ""


def test_reconstruct_layout_single_line():
    """Test layout reconstruction with items on a single line."""
    # Simulate OCR output: [[bbox_points], (text, confidence)]
    # bbox_points: [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
    ocr_result = [[
        [[[10, 100], [50, 100], [50, 120], [10, 120]], ("Date", 0.99)],
        [[[60, 100], [150, 100], [150, 120], [60, 120]], ("Description", 0.99)],
        [[[160, 100], [200, 100], [200, 120], [160, 120]], ("Amount", 0.99)],
    ]]

    result = _reconstruct_layout(ocr_result)
    assert "Date" in result
    assert "Description" in result
    assert "Amount" in result
    # All items should be on the same line (joined by tabs)
    assert result.count("\n") == 0


def test_reconstruct_layout_multiple_lines():
    """Test layout reconstruction with items on multiple lines."""
    ocr_result = [[
        # Header row (y ~= 100)
        [[[10, 100], [50, 100], [50, 120], [10, 120]], ("Date", 0.99)],
        [[[60, 100], [150, 100], [150, 120], [60, 120]], ("Amount", 0.99)],
        # Data row 1 (y ~= 150)
        [[[10, 150], [80, 150], [80, 170], [10, 170]], ("2024-01-15", 0.98)],
        [[[60, 150], [120, 150], [120, 170], [60, 170]], ("-85.50", 0.98)],
        # Data row 2 (y ~= 200)
        [[[10, 200], [80, 200], [80, 220], [10, 220]], ("2024-01-16", 0.97)],
        [[[60, 200], [120, 200], [120, 220], [60, 200]], ("-45.00", 0.97)],
    ]]

    result = _reconstruct_layout(ocr_result)
    lines = result.split("\n")

    assert len(lines) == 3
    assert "Date" in lines[0]
    assert "Amount" in lines[0]
    assert "2024-01-15" in lines[1]
    assert "2024-01-16" in lines[2]


def test_reconstruct_layout_preserves_reading_order():
    """Test that items within a line are sorted left to right."""
    # Items intentionally out of order by X position
    ocr_result = [[
        [[[200, 100], [250, 100], [250, 120], [200, 120]], ("Third", 0.99)],
        [[[10, 100], [50, 100], [50, 120], [10, 120]], ("First", 0.99)],
        [[[100, 100], [150, 100], [150, 120], [100, 120]], ("Second", 0.99)],
    ]]

    result = _reconstruct_layout(ocr_result)
    parts = result.split("\t")

    assert parts[0] == "First"
    assert parts[1] == "Second"
    assert parts[2] == "Third"


def test_load_pdf_file_with_mocked_ocr():
    """Test PDF loading with mocked PaddleOCR to avoid slow actual OCR."""
    mock_ocr_result = [[
        [[[10, 50], [100, 50], [100, 70], [10, 70]], ("Bank Statement", 0.99)],
        [[[10, 100], [50, 100], [50, 120], [10, 120]], ("Date", 0.99)],
        [[[60, 100], [150, 100], [150, 120], [60, 120]], ("Description", 0.99)],
        [[[160, 100], [200, 100], [200, 120], [160, 120]], ("Amount", 0.99)],
    ]]

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        temp_path = f.name

    try:
        with patch("src.parsers.pdf._get_ocr_engine") as mock_get_ocr:
            mock_ocr = MagicMock()
            mock_ocr.ocr.return_value = [mock_ocr_result[0]]
            mock_get_ocr.return_value = mock_ocr

            result = load_pdf(temp_path)

            assert "Bank Statement" in result
            assert "Date" in result
            assert "Description" in result
            assert "Amount" in result
            assert "Page 1" in result
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
            patch("src.parsers.pdf_llm.ChatOpenAI") as mock_chat_class,
        ):
            mock_pdf_to_images.return_value = [mock_image]
            mock_llm = MagicMock()
            mock_llm.invoke.return_value = mock_llm_response
            mock_chat_class.return_value = mock_llm

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
            patch("src.parsers.pdf_llm.ChatOpenAI") as mock_chat_class,
        ):
            mock_pdf_to_images.return_value = mock_images
            mock_llm = MagicMock()
            mock_llm.invoke.side_effect = [page1_response, page2_response]
            mock_chat_class.return_value = mock_llm

            result = load_pdf_with_llm(temp_path)

            assert "Page 1" in result
            assert "Page 2" in result
            assert "Transaction A" in result
            assert "Transaction B" in result

            # Verify LLM was called twice (once per page)
            assert mock_llm.invoke.call_count == 2
    finally:
        Path(temp_path).unlink()
