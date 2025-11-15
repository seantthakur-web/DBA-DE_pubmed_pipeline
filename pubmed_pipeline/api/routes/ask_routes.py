from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pubmed_pipeline.agents.base.langgraph_env import build_graph
import uuid
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Request model
class AskRequest(BaseModel):
    query: str
    top_k: int = 5

# Response wrapper (optional – FastAPI will serialize dict)
class AskResponse(BaseModel):
    trace_id: str
    final: dict

@router.post("/ask", response_model=dict)
async def ask_endpoint(req: AskRequest):
    """
    Runs the LangGraph pipeline and returns its final output as JSON.
    """

    try:
        trace_id = str(uuid.uuid4())

        graph = build_graph()
        logger.info(f"[trace_id={trace_id}] Starting graph execution")

        # The graph expects a dict state
        initial_state = {
            "trace_id": trace_id,
            "query": req.query,
            "top_k": req.top_k,
        }

        # Run LangGraph
        final_state = graph.invoke(initial_state)

        logger.info(f"[trace_id={trace_id}] Graph execution complete")

        if not isinstance(final_state, dict):
            raise ValueError("Graph returned a non-dict state.")

        return final_state

    except Exception as e:
        logger.exception(f"/ask failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
