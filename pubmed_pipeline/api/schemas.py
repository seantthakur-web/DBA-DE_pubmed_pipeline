from typing import List, Optional, Any
from pydantic import BaseModel


# -----------------------------
# Request Schema
# -----------------------------
class AskRequest(BaseModel):
    """
    Incoming request to /api/ask.
    """
    query: str
    top_k: Optional[int] = 5


# -----------------------------
# Response Schema
# -----------------------------
class AskResponse(BaseModel):
    """
    Structured response returned by LangGraph pipeline.
    Mirrors the AgentState output.
    """
    trace_id: Optional[str]
    query: str
    intent: Optional[str]

    summaries: Optional[List[Any]]
    insights: Optional[List[Any]]

    final_answer: Optional[str]

    execution_order: Optional[List[str]]
    used_llm: Optional[bool]

    # List of retrieved PubMed docs (dicts: pmid, chunk_id, text, score)
    retrieved_docs: Optional[List[dict]]
