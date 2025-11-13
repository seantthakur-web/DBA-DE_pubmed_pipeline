"""
schemas.py
Pydantic models used across the FastAPI layer.
"""

from __future__ import annotations

from pydantic import BaseModel
from typing import Any, Dict, List, Optional


# ============================================================
# Request Model for /api/ask
# ============================================================

class AskRequest(BaseModel):
    """
    POST /api/ask
    """
    query: str


# ============================================================
# Response Model for /api/ask
# ============================================================

class AskResponse(BaseModel):
    """
    Unified response for a full LangGraph pipeline run.
    """
    trace_id: str
    summary: Optional[str]
    insights: Optional[List[Any]]
    retrieved_docs: Optional[List[Dict[str, Any]]]
    final_answer: Optional[str]
    artifacts: Dict[str, str]
    metadata: Dict[str, Any]


# ============================================================
# (Optional) You may add more models later if needed
# ============================================================
