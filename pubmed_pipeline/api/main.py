# pubmed_pipeline/api/main.py

"""
FastAPI backend for the PubMed RAG + LangGraph application.
Implements a production-ready /api/ask endpoint with logging & traceability.
"""

import logging
import os
import time
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from pubmed_pipeline.agents.base.langgraph_env import run_graph
from pubmed_pipeline.rag.artifact_generator import save_artifact


# -----------------------------------------------------------------------------
# Logging Setup for API (INNVO-504)
# -----------------------------------------------------------------------------

logger = logging.getLogger("pubmed_api")
logger.setLevel(logging.INFO)

# Avoid duplicate handlers when using --reload
if not logger.handlers:
    os.makedirs("pubmed_pipeline/logs/api", exist_ok=True)
    log_path = "pubmed_pipeline/logs/api/api_server.log"

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    logger.info("API logger initialized. Writing to %s", log_path)


# -----------------------------------------------------------------------------
# Request / Response Schemas
# -----------------------------------------------------------------------------

class AskRequest(BaseModel):
    query: str
    top_k: int = 5


class RetrievedDoc(BaseModel):
    pmid: str
    chunk_id: int
    text: str
    score: Optional[float] = None


class AskResponse(BaseModel):
    trace_id: str
    query: str
    intent: str

    execution_order: List[str] = []
    summaries: Optional[List[str]] = None
    insights: Optional[List[str]] = None

    retrieved_docs: List[RetrievedDoc] = []
    final_answer: Optional[str] = None


# -----------------------------------------------------------------------------
# FastAPI App Initialization
# -----------------------------------------------------------------------------

app = FastAPI(
    title="PubMed RAG + LangGraph API",
    version="0.1.0",
    description="End-to-end backend for the PubMed multi-agent RAG pipeline.",
)

# MVP CORS (tighten later for pilot)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # Restrict later to Streamlit domain or specific origins
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# -----------------------------------------------------------------------------
# Health Check
# -----------------------------------------------------------------------------

@app.get("/health")
def health_check():
    logger.info("Health check called.")
    return {"status": "ok"}


# -----------------------------------------------------------------------------
# Core Endpoint — /api/ask
# -----------------------------------------------------------------------------

@app.post("/api/ask", response_model=AskResponse)
def ask_pubmed(request: AskRequest) -> AskResponse:
    """
    Main endpoint that executes the LangGraph multi-agent pipeline and returns
    the final AgentState to the UI.

    Logs:
    - Incoming query + top_k
    - Total latency
    - Execution order
    - #retrieved_docs
    - Errors with traceback
    """
    start_time = time.perf_counter()
    logger.info(
        "Received /api/ask | query='%s' | top_k=%d",
        request.query,
        request.top_k,
    )

    try:
        # Run LangGraph
        state = run_graph(request.query, request.top_k)

        # Unified dictionary conversion
        if hasattr(state, "model_dump"):
            data = state.model_dump()
        else:
            data = state  # fallback if graph returned dict-like

        trace_id = data.get("trace_id", "n/a")
        execution_order = data.get("execution_order", [])
        summaries = data.get("summaries")
        insights = data.get("insights")
        final_answer = data.get("final_answer")

        # Build response skeleton
        response = AskResponse(
            trace_id=trace_id,
            query=data.get("query", request.query),
            intent=data.get("intent", "answer"),
            execution_order=execution_order,
            summaries=summaries,
            insights=insights,
            final_answer=final_answer,
            retrieved_docs=[],
        )

        # Map retrieved_docs → Pydantic RetrievedDoc objects
        raw_docs = data.get("retrieved_docs") or []
        for d in raw_docs:
            # Support dicts or simple objects
            pmid = d.get("pmid") if isinstance(d, dict) else getattr(d, "pmid", None)
            chunk_id = d.get("chunk_id") if isinstance(d, dict) else getattr(d, "chunk_id", None)
            text = d.get("text") if isinstance(d, dict) else getattr(d, "text", None)
            score = d.get("score") if isinstance(d, dict) else getattr(d, "score", None)

            if pmid is None or chunk_id is None or text is None:
                continue

            response.retrieved_docs.append(
                RetrievedDoc(
                    pmid=str(pmid),
                    chunk_id=int(chunk_id),
                    text=str(text),
                    score=score if score is not None else None,
                )
            )

        # Save artifact (INNVO-503)
        artifact_path = save_artifact(response)

        duration_ms = (time.perf_counter() - start_time) * 1000.0
        logger.info(
            "Completed /api/ask | trace_id=%s | latency_ms=%.1f | exec_order=%s | retrieved_docs=%d | artifact=%s",
            trace_id,
            duration_ms,
            "→".join(execution_order),
            len(response.retrieved_docs),
            artifact_path,
        )

        return response

    except HTTPException:
        # Already formatted HTTP error
        raise

    except Exception as e:
        duration_ms = (time.perf_counter() - start_time) * 1000.0
        logger.exception(
            "Unhandled exception in /api/ask | latency_ms=%.1f | error=%s",
            duration_ms,
            str(e),
        )
        raise HTTPException(status_code=500, detail="Internal server error.")
