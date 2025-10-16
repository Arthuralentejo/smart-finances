# Personal Finance Manager (PFM)

A proof-of-concept Personal Finance Manager that uses LLMs to extract and normalize transaction data from bank statements, enabling natural language queries of your financial data.

## Features

- Upload PDF or CSV bank statements
- Automatic transaction extraction using LLMs
- Normalized data storage in SQLite
- Natural language chat interface for financial queries
- Transaction analytics and insights

## Tech Stack

- **Python 3.11+**
- **Streamlit** - Frontend interface
- **LangGraph** - Workflow orchestration
- **LangChain** - LLM integration
- **Pydantic** - Data validation
- **SQLite** - Database
- **Pandas** - Data processing
- **Unstructured** - PDF parsing

## Setup

1. Clone the repository

2. Install dependencies with Poetry:
   ```bash
   poetry install
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

4. Run the application:
   ```bash
   poetry run streamlit run src/ui/app.py
   ```

   Or activate the Poetry shell first:
   ```bash
   poetry shell
   streamlit run src/ui/app.py
   ```

## Usage

1. Upload a bank statement (PDF or CSV format)
2. The system will automatically extract and normalize transactions
3. View your transactions in the table
4. Use the chat interface to ask questions about your finances

## Project Structure

See [project_plan.md](project_plan.md) for detailed architecture and implementation plan.

## License

MIT
