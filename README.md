# Personal Finance Manager (PFM)

A proof-of-concept Personal Finance Manager that uses LLMs to extract and normalize transaction data from bank statements, enabling natural language queries of your financial data.

## Features

- Upload PDF or CSV bank statements
- Automatic transaction extraction using LLM agents
- Intelligent transaction categorization with web search (Tavily)
- Normalized data storage in SQLite
- Natural language chat interface for financial queries
- RESTful API backend with FastAPI
- Streamlit frontend

## Tech Stack

- **Python 3.11+**
- **FastAPI** - Backend API
- **Streamlit** - Frontend interface
- **LangGraph** - Workflow orchestration
- **LangChain** - LLM agents and tools
- **PaddleOCR** - PDF text extraction
- **Tavily** - Web search for transaction categorization
- **Pydantic** - Data validation
- **SQLAlchemy + SQLite** - Database
- **Docker** - Containerization

## Architecture

The application uses a graph-based processing pipeline:

```
File Upload → Extractor Agent → Categorizer Agent → Database Saver
                   │                    │
                   ▼                    ▼
            CSV/PDF Tools         Tavily Search
```

## Quick Start

### Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/docs/#installation)
- Docker (optional, for containerized deployment)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd smart-finances

# Install dependencies
make install
```

### Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and configure required variables:
# - OPENAI_API_KEY: Your OpenAI API key
# - TAVILY_API_KEY: Your Tavily API key (for transaction categorization)
```

### Running the Application

#### Option 1: Local Development

```bash
# Terminal 1: Start the FastAPI backend
make run-api

# Terminal 2: Start the Streamlit frontend
make run-ui
```

The API will be available at `http://localhost:8000` and the UI at `http://localhost:8501`.

#### Option 2: Docker

```bash
# Build and start all containers
make docker-up

# Or run in background
make docker-up-d

# View logs
make docker-logs

# Stop containers
make docker-down
```

## Available Commands

Run `make help` to see all available commands:

### Setup
| Command | Description |
|---------|-------------|
| `make install` | Install dependencies with Poetry |

### Development
| Command | Description |
|---------|-------------|
| `make run-api` | Run the FastAPI backend (port 8000) |
| `make run-ui` | Run the Streamlit frontend (port 8501) |

### Testing & Quality
| Command | Description |
|---------|-------------|
| `make test` | Run all tests |
| `make test-cov` | Run tests with coverage report |
| `make lint` | Run linter (ruff) |
| `make lint-fix` | Run linter and auto-fix issues |
| `make format` | Format code (ruff) |
| `make type-check` | Run type checker (mypy) |
| `make check` | Run all checks (lint, type-check, test) |

### Docker
| Command | Description |
|---------|-------------|
| `make docker-build` | Build Docker images |
| `make docker-up` | Start containers in foreground |
| `make docker-up-d` | Start containers in background |
| `make docker-down` | Stop containers |
| `make docker-logs` | View container logs |
| `make docker-clean` | Stop containers and remove volumes |

### Cleanup
| Command | Description |
|---------|-------------|
| `make clean` | Remove cache and build artifacts |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/process` | Upload and process a bank statement |
| POST | `/chat` | Query transactions with natural language |

## Project Structure

```
smart-finances/
├── src/
│   ├── api/              # FastAPI application
│   │   ├── routes/       # API route handlers
│   │   ├── dependencies.py
│   │   ├── main.py
│   │   └── schemas.py
│   ├── database/         # SQLAlchemy models and operations
│   ├── graphs/           # LangGraph workflows
│   │   ├── nodes/        # Graph node implementations
│   │   │   ├── extractor_node/   # File loading & extraction agent
│   │   │   ├── categorizer_node/ # Transaction categorization agent
│   │   │   └── node_saver.py     # Database persistence
│   │   ├── graph_processing.py
│   │   └── state.py
│   ├── llm/              # LLM client configuration
│   ├── models/           # Pydantic models
│   ├── parsers/          # File parsers (CSV, PDF, OCR)
│   ├── settings/         # Application configuration
│   └── ui/               # Streamlit frontend
├── tests/                # Test suite
├── docker/               # Docker configuration
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
├── Makefile              # Build and run commands
├── pyproject.toml        # Project dependencies
└── README.md
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key for LLM calls |
| `TAVILY_API_KEY` | Yes | Tavily API key for web search |
| `DATABASE_URL` | No | SQLite path (default: `sqlite:///data/database/pfm.db`) |
| `LLM_MODEL` | No | Model to use (default: `gpt-4o-mini`) |

## License

MIT
