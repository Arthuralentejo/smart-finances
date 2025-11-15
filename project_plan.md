# Personal Finance Manager (PFM) - Project Plan

## Overview
A Personal Finance Manager that uses LLMs to extract and normalize transaction data from bank statements (PDF/CSV), stores them in SQLite, and enables natural language querying of financial data.

## Tech Stack
- **Python**: 3.11+
- **Frontend**: Streamlit
- **Orchestration**: LangGraph
- **LLM Logic**: LangChain
- **Validation**: Pydantic
- **Database**: SQLite
- **Data Processing**: Pandas, Unstructured

## Architecture Components

### 1. Data Models (Pydantic)
- `Transaction`: Normalized transaction schema
  - id, date, description, amount, category, account, balance
- `BankStatement`: Metadata for uploaded statements
- `ExtractionResult`: LLM extraction output wrapper

### 2. Database Layer (SQLAlchemy + SQLite)
- `transactions` table
- `statements` table
- CRUD operations for transactions
- Query interface for chat functionality

### 3. Document Processing Pipeline
- **PDF Parser**: Extract text from PDF statements using Unstructured
- **CSV Parser**: Read and normalize CSV files with Pandas
- **LLM Extractor**: Use LangChain to structure extraction prompts
- **Normalizer**: Convert raw extractions to Pydantic models

### 4. LangGraph Orchestration
- **Statement Processing Graph**:
  1. File Upload Node
  2. Format Detection Node
  3. Text Extraction Node
  4. LLM Normalization Node
  5. Validation Node
  6. Database Save Node
  7. Error Handling Node

- **Chat Query Graph**:
  1. User Question Node
  2. Query Generation Node
  3. Database Retrieval Node
  4. Response Generation Node

### 5. Streamlit Frontend
- **Upload Page**: Drag-and-drop for PDF/CSV
- **Transactions View**: Table display with filters
- **Chat Interface**: Natural language queries
- **Analytics Dashboard**: Basic spending insights

## Implementation Steps

### Phase 1: Project Setup
1. Create folder structure
2. Set up virtual environment
3. Install dependencies
4. Configure environment variables (.env)

### Phase 2: Core Data Layer
1. Define Pydantic models for transactions
2. Create SQLAlchemy models and database schema
3. Implement database initialization and CRUD operations
4. Write database utility functions

### Phase 3: Document Processing
1. Implement PDF text extraction using Unstructured
2. Implement CSV parsing with Pandas
3. Create format detection logic
4. Build preprocessing utilities

### Phase 4: LLM Integration
1. Set up LangChain with OpenAI
2. Create extraction prompts for transaction normalization
3. Implement LLM-based transaction parser
4. Add validation and error handling for LLM outputs

### Phase 5: LangGraph Orchestration
1. Design statement processing workflow graph
2. Implement graph nodes for each processing step
3. Add state management and error recovery
4. Create chat query workflow graph

### Phase 6: Streamlit UI
1. Build file upload interface
2. Create transaction display table
3. Implement chat interface
4. Add basic analytics visualizations
5. Create navigation and session state management

### Phase 7: Integration & Testing
1. Connect all components end-to-end
2. Test with sample bank statements
3. Add error handling and user feedback
4. Optimize LLM prompts for accuracy

### Phase 8: Enhancement (Optional)
1. Add transaction categorization
2. Implement spending trends
3. Add export functionality
4. Create budget tracking features

## File Structure
```
smart-finances/
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── transaction.py      # Pydantic models
│   │   └── database.py          # SQLAlchemy models
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py        # DB setup
│   │   └── operations.py        # CRUD operations
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── pdf_parser.py
│   │   └── csv_parser.py
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── extractor.py         # LLM extraction logic
│   │   └── prompts.py           # Prompt templates
│   ├── graphs/
│   │   ├── __init__.py
│   │   ├── processing_graph.py  # Statement processing
│   │   └── chat_graph.py        # Chat workflow
│   └── ui/
│       ├── __init__.py
│       └── app.py               # Streamlit main app
├── data/
│   ├── uploads/                 # Temp uploaded files
│   ├── database/                # SQLite DB
│   └── samples/                 # Sample statements
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── project_plan.md
```

## Key Considerations

### LLM Prompt Design
- Provide clear examples of desired JSON output format
- Handle multiple statement formats gracefully
- Include few-shot examples for better accuracy

### Error Handling
- Invalid file formats
- Failed LLM extractions
- Duplicate transaction detection
- Database connection errors

### Data Quality
- Validate transaction dates, amounts
- Handle missing or malformed data
- Provide user feedback on extraction confidence

### Performance
- Stream large PDFs in chunks
- Batch database inserts
- Cache LLM responses where applicable

## Environment Variables
- `OPENAI_API_KEY`: OpenAI API key for LLM calls
- `DATABASE_URL`: SQLite database path (default: data/database/pfm.db)
- `UPLOAD_FOLDER`: Temporary upload directory
- `LLM_MODEL`: Model to use (default: gpt-4o-mini)

## Next Steps
1. Set up development environment
2. Start with Phase 2 (Core Data Layer)
3. Build incrementally, testing each component
4. Iterate on LLM prompts based on real statement samples
