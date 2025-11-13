from pydantic import BaseModel, Field
from typing import List, Optional


class QueryRequest(BaseModel):
    query: str = Field(..., description="User natural-language question")
    workflow: Optional[str] = Field(
        "router_summarizer_raganswer_reporter",
        description="Workflow to execute"
    )


class NextRequest(BaseModel):
    workflow: str = Field(..., description="Workflow name to load")


class QueryResponse(BaseModel):
    answer: Optional[str]
    summary: Optional[str]
    insights: Optional[str]
    citations: Optional[List[str]]
    debug: Optional[dict]
    metadata: Optional[dict]
    trace_id: Optional[str]
