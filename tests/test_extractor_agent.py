"""Tests for the extractor agent tools."""

import tempfile
from pathlib import Path
from unittest.mock import patch

from src.graphs.nodes.extractor_node.tools import create_extractor_tools


def test_create_extractor_tools():
    """Test that extractor tools are created correctly."""
    tools = create_extractor_tools()

    assert len(tools) == 2

    tool_names = [tool.name for tool in tools]
    assert "load_csv_file" in tool_names
    assert "load_pdf_file" in tool_names


def test_load_csv_tool():
    """Test that the CSV tool loads files correctly."""
    tools = create_extractor_tools()
    csv_tool = next(t for t in tools if t.name == "load_csv_file")

    csv_content = "date,description,amount\n2024-01-15,Grocery Store,-85.50"

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(csv_content)
        temp_path = f.name

    try:
        result = csv_tool.invoke({"file_path": temp_path})

        assert "date" in result
        assert "description" in result
        assert "amount" in result
        assert "Grocery Store" in result
    finally:
        Path(temp_path).unlink()


def test_load_pdf_tool_calls_ocr_service():
    """Test that the PDF tool calls the OCR service."""
    from unittest.mock import AsyncMock

    # Need to patch before creating tools since load_pdf is imported at module level
    with patch(
        "src.graphs.nodes.extractor_node.tools.load_pdf",
        new_callable=AsyncMock,
        return_value="Extracted PDF content",
    ) as mock_load_pdf:
        tools = create_extractor_tools()
        pdf_tool = next(t for t in tools if t.name == "load_pdf_file")

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            temp_path = f.name

        try:
            result = pdf_tool.invoke({"file_path": temp_path})

            assert result == "Extracted PDF content"
            mock_load_pdf.assert_called_once_with(temp_path)
        finally:
            Path(temp_path).unlink()
