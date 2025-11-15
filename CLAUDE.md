# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal Finance Manager (PFM) - A POC that uses LLMs to extract and normalize transaction data from bank statements (PDF/CSV), stores them in SQLite, and enables natural language querying.

## Commands

Run `make help` to see all available commands. Key commands:

```bash
# Setup
make install          # Install dependencies

# Development
make run-api          # Run FastAPI backend (port 8000)
make run-ui           # Run Streamlit frontend (port 8501)

# Testing & Quality
make test             # Run all tests
make test-cov         # Run tests with coverage
make lint             # Run linter (ruff)
make lint-fix         # Auto-fix lint errors
make format           # Format code (ruff)
make type-check       # Run type checker (mypy)
make check            # Run all checks (lint, type-check, test)

# Docker
make docker-up        # Build and start containers
make docker-up-d      # Start in background
make docker-down      # Stop containers
make docker-logs      # View logs
make docker-clean     # Stop and remove volumes

# Cleanup
make clean            # Remove cache files
```

## Architecture

The application is split into a **FastAPI backend** and a **Streamlit frontend**, each running in separate Docker containers.

### Docker Services

- **backend** - FastAPI API server (port 8000)
  - Handles document processing and chat queries
  - Includes PaddleOCR for PDF extraction
  - Persists data to a Docker volume
- **frontend** - Streamlit web UI (port 8501)
  - Communicates with backend via HTTP
  - Depends on backend health check

### Backend API Endpoints

- `POST /process` - Upload and process a bank statement (PDF/CSV)
- `POST /chat` - Natural language query about transaction data
- `GET /health` - Health check endpoint

### LangGraph Workflows

**Statement Processing Graph**: File Upload → Format Detection → Text Extraction → LLM Normalization → Validation → Database Save

**Chat Query Graph**: User Question → Query Generation → Database Retrieval → Response Generation

### Key Components

- **src/api/**: FastAPI backend application
  - `main.py` - Application entry point
  - `schemas.py` - API request/response models
  - `routes/` - API route handlers
- **src/models/**: Pydantic models (`Transaction`, `TransactionList`)
- **src/database/**: SQLite connection and CRUD operations (SQLAlchemy)
- **src/parsers/**: PDF extraction (PaddleOCR) and CSV parsing (Pandas)
- **src/llm/**: LangChain integration for transaction extraction
  - `client.py` - LLM client initialization
  - `extractor.py` - Transaction extraction chain
- **src/graphs/**: LangGraph workflows
  - `processing.py` - Statement processing workflow
  - `chat.py` - Chat agent for natural language queries
- **src/ui/**: Streamlit frontend (calls backend API)

### Environment Variables

Required in `.env`:
- `OPENAI_API_KEY` - OpenAI API key for LLM calls
- `DATABASE_URL` - SQLite path (default: `sqlite:///data/database/pfm.db`)
- `LLM_MODEL` - Model to use (default: `gpt-4o-mini`)
- `API_URL` - Backend API URL for frontend (default: `http://localhost:8000`)
