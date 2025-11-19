from fastapi import APIRouter, HTTPException
from pubmed_pipeline.agents.base.langgraph_env import run_pipeline
from pubmed_pipeline.api.schemas import AskRequest, AskResponse
from pubmed_pipeline.utils.log_config import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    """
    Main RAG endpoint.
    Calls router → rag_answer → END via LangGraph.
    """

    try:
        query = request.query
        top_k = request.top_k or 5

        logger.info(f"[API] /ask received query: {query}")

        # Execute agent pipeline
        final_state = run_pipeline(query=query, top_k=top_k)

        # Convert AgentState into AskResponse Pydantic model
        response = AskResponse(
            trace_id=final_state.trace_id,
            query=final_state.query,
            intent=final_state.intent,
            summaries=final_state.summaries,
            insights=final_state.insights,
            final_answer=final_state.final_answer,
            execution_order=final_state.execution_order,
            used_llm=final_state.used_llm,
            retrieved_docs=final_state.retrieved_docs,
        )

        return response

    except Exception as e:
        logger.exception(f"[API] /ask failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
