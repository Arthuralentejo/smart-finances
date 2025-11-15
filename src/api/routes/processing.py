"""Document processing API routes."""

import tempfile
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from src.api.dependencies import ProcessingGraphDep
from src.api.schemas import SUPPORTED_FILE_TYPES, ProcessingResponse, TransactionResponse

router = APIRouter(prefix="/process", tags=["processing"])


@router.post("", response_model=ProcessingResponse)
async def process_document(
    graph: ProcessingGraphDep,
    file: UploadFile = File(...),
) -> ProcessingResponse:
    """Process an uploaded bank statement (PDF or CSV).

    Extracts transactions from the document and saves them to the database.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    extension = Path(file.filename).suffix.lower()
    if extension not in SUPPORTED_FILE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format: {extension}. Supported formats: {SUPPORTED_FILE_TYPES}",
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        result = graph.invoke({"file_path": tmp_path})

        transactions = [
            TransactionResponse(
                date=txn.date,
                merchant=txn.merchant,
                description=txn.description,
                amount=txn.amount,
                category=txn.category,
            )
            for txn in result["transactions"]
        ]

        return ProcessingResponse(
            success=True,
            message=f"Successfully processed {file.filename}",
            transactions=transactions,
            transaction_count=len(transactions),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        Path(tmp_path).unlink(missing_ok=True)
