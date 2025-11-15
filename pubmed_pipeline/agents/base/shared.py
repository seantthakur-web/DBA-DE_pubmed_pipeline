"""
shared.py
Shared pydantic AgentState for all LangGraph nodes.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class AgentState(BaseModel):
    """
    Core state object shared by all agents in the LangGraph pipeline.
    Supports both partial updates (via extra='allow') and deterministic fallback mode.
    """

    # User query
    query: str = ""

    # Routing field (set by RouterAgent)
    route: Optional[str] = None

    # Outputs from summarizer, reporter, and RAGAnswer
    summary: Optional[str] = None
    insights: Optional[List[str]] = None
    retrieved_docs: Optional[List[Dict[str, Any]]] = None
    final_answer: Optional[str] = None

    # Metadata
    trace_id: Optional[str] = None
    node_sequence: List[str] = Field(default_factory=list)
    timestamps: Dict[str, float] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"
