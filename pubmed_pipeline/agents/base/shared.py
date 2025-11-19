from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class AgentState(BaseModel):
    # Core request metadata
    trace_id: str
    query: str
    intent: str

    # Retrieval outputs
    retrieved_docs: List[Dict[str, Any]] = Field(default_factory=list)
    top_k: int = 5

    # Agent outputs
    summaries: List[str] = Field(default_factory=list)
    insights: List[str] = Field(default_factory=list)
    final_answer: Optional[str] = None

    # Execution bookkeeping
    execution_order: List[str] = Field(default_factory=list)
    used_llm: bool = False
