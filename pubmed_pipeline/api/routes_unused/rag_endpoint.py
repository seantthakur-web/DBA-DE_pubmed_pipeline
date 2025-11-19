"""
rag_endpoint.py
FastAPI route to expose the LangGraph DAGController as /api/ask.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pubmed_pipeline.api.schemas import AskRequest, AskResponse
from pubmed_pipeline.agents.base.dag_controller import DAGController
from pubmed_pipeline.agents.base.shared import logger

router = APIRouter(prefix="/api", tags=["rag"])

# Compile DAGController once at import time
controller = DAGController()


@router.post("/ask", response_model=AskResponse)
def ask_pubmed(request: AskRequest):
    """
    Execute the full LangGraph workflow for a given query.
    """
    query = request.query

    if not query or not isinstance(query, str) or not query.strip():
        raise HTTPException(status_code=400, detail="Query must be a non-empty string.")

    logger.info("FastAPI /api/ask — received query=%r", query)

    # Run DAG (returns: {trace_id, result, metadata, artifacts})
    output = controller.run(query, debug=False)

    trace_id = output.get("trace_id")
    result = output.get("result", {})
    metadata = output.get("metadata", {})
    artifacts = output.get("artifacts", {})

    if not trace_id:
        raise HTTPException(status_code=500, detail="Pipeline returned no trace_id.")

    return {
        "trace_id": trace_id,
        "summary": result.get("summary"),
        "insights": result.get("insights"),
        "retrieved_docs": result.get("retrieved_docs"),
        "final_answer": result.get("final_answer"),
        "artifacts": artifacts,
        "metadata": metadata,
    }
