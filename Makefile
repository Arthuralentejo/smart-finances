.PHONY: help install run-api run-ui run test lint format type-check clean docker-build docker-up docker-down docker-logs docker-clean

# Default target
help:
	@echo "Personal Finance Manager - Available Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install       Install dependencies with Poetry"
	@echo ""
	@echo "Development:"
	@echo "  make run-api       Run the FastAPI backend (port 8000)"
	@echo "  make run-ui        Run the Streamlit frontend (port 8501)"
	@echo "  make run           Run both API and UI (requires 'make run-api' in another terminal)"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test          Run all tests"
	@echo "  make test-cov      Run tests with coverage report"
	@echo "  make lint          Run linter (ruff)"
	@echo "  make format        Format code (ruff)"
	@echo "  make type-check    Run type checker (mypy)"
	@echo "  make check         Run all checks (lint, type-check, test)"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build  Build Docker images"
	@echo "  make docker-up     Start containers in foreground"
	@echo "  make docker-up-d   Start containers in background"
	@echo "  make docker-down   Stop containers"
	@echo "  make docker-logs   View container logs"
	@echo "  make docker-clean  Stop containers and remove volumes"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean         Remove cache and build artifacts"

# ============================================================================
# Setup
# ============================================================================

install:
	poetry install

# ============================================================================
# Development
# ============================================================================

run-api:
	poetry run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

run-ui:
	poetry run streamlit run src/ui/app.py --server.port 8501

run: run-ui

# ============================================================================
# Testing & Quality
# ============================================================================

test:
	poetry run pytest -v

test-cov:
	poetry run pytest -v --cov=src --cov-report=html --cov-report=term

lint:
	poetry run ruff check src/ tests/

lint-fix:
	poetry run ruff check src/ tests/ --fix

format:
	poetry run ruff format src/ tests/

format-check:
	poetry run ruff format src/ tests/ --check

type-check:
	poetry run mypy src/

check: lint type-check test

# ============================================================================
# Docker
# ============================================================================

docker-build:
	docker compose -f docker/docker-compose.yml build

docker-up:
	docker compose -f docker/docker-compose.yml up --build

docker-up-d:
	docker compose -f docker/docker-compose.yml up -d --build

docker-down:
	docker compose -f docker/docker-compose.yml down

docker-logs:
	docker compose -f docker/docker-compose.yml logs -f

docker-clean:
	docker compose -f docker/docker-compose.yml down -v --rmi local

# ============================================================================
# Cleanup
# ============================================================================

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
