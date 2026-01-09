"""Tests for FastAPI endpoints."""

import tempfile
from datetime import date
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.api.dependencies import get_processing_graph
from src.api.main import app
from src.models import Transaction


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_graph():
    """Create a mock processing graph."""
    return MagicMock()


@pytest.fixture
def client_with_mock_graph(mock_graph):
    """Create a test client with mocked processing graph."""

    def override_graph():
        return mock_graph

    app.dependency_overrides[get_processing_graph] = override_graph

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_process_unsupported_format(client):
    """Test that processing rejects unsupported file formats."""
    # Create a temporary .txt file
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        f.write(b"some text content")
        temp_path = f.name

    try:
        with open(temp_path, "rb") as f:
            response = client.post(
                "/process",
                files={"file": ("test.txt", f, "text/plain")},
            )
        assert response.status_code == 400
        assert "Unsupported file format" in response.json()["detail"]
    finally:
        Path(temp_path).unlink()


def test_process_csv_with_mocked_graph(client_with_mock_graph, mock_graph):
    """Test CSV processing with mocked graph execution."""
    # Create mock transactions
    mock_transactions = [
        Transaction(
            transaction_date=date(2024, 1, 15),
            merchant="Grocery Store",
            description="Weekly groceries",
            amount=-85.50,
            category="Food",
        ),
    ]

    mock_graph.invoke.return_value = {
        "transactions": mock_transactions,
        "status": "saved",
    }

    csv_content = b"date,description,amount\n2024-01-15,Grocery Store,-85.50"

    response = client_with_mock_graph.post(
        "/process",
        files={"file": ("test.csv", csv_content, "text/csv")},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["transaction_count"] == 1
    assert len(data["transactions"]) == 1
    assert data["transactions"][0]["merchant"] == "Grocery Store"

    # Verify graph was called
    mock_graph.invoke.assert_called_once()


def test_chat_endpoint_with_mocked_response(client):
    """Test chat endpoint with mocked analyst response."""
    with patch("src.api.routes.chat.get_analyst_response") as mock_analyst:
        mock_analyst.return_value = "You spent $85.50 on groceries."

        response = client.post(
            "/chat",
            json={"query": "How much did I spend on groceries?"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "groceries" in data["response"].lower()


def test_chat_endpoint_empty_query(client):
    """Test that chat endpoint rejects empty queries."""
    response = client.post(
        "/chat",
        json={"query": ""},
    )
    assert response.status_code == 422  # Validation error
