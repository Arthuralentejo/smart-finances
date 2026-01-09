"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from logging import getLogger

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import chat, processing
from src.graphs import build_processing_graph
from src.parsers import OCRClient
from src.settings.config import settings

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager.

    Initializes resources on startup and cleans up on shutdown.
    """
    client = httpx.AsyncClient(
        base_url=settings.ocr_service_base_url, timeout=settings.ocr_service_timeout
    )
    ocr_client = OCRClient(client)
    processing_graph = build_processing_graph(ocr_client)
    logger.debug("Application startup complete")

    try:
        yield {"processing_graph": processing_graph}
    finally:
        await ocr_client.aclose()
        logger.debug("Application shutdown complete")


app = FastAPI(
    title="Personal Finance Manager API",
    description="API for processing bank statements and querying transaction data",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(processing.router)
app.include_router(chat.router)


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}
