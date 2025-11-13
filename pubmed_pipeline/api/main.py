"""
main.py
Entry point for the FastAPI application.
"""

from fastapi import FastAPI
from .routes.rag_endpoint import router as rag_router

# Initialize FastAPI app
app = FastAPI(
    title="PubMed AI Pipeline",
    description="FastAPI interface for LangGraph-powered biomedical RAG pipeline.",
    version="1.0.0",
)

# Register API routes
app.include_router(rag_router)


# Optional health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}
