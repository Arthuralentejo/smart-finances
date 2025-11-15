"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import chat, processing
from src.graphs import build_processing_graph


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager.

    Initializes resources on startup and cleans up on shutdown.
    """
    processing_graph = build_processing_graph()

    yield {"processing_graph": processing_graph}


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
