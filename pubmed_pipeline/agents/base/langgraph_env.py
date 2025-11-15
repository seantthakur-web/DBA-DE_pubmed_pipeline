import uuid
from typing import List, Optional

from pydantic import BaseModel, Field
from langgraph.graph import StateGraph

from pubmed_pipeline.agents.router.router_agent import RouterAgent
from pubmed_pipeline.agents.summarizer.summarizer_agent import SummarizerAgent
from pubmed_pipeline.agents.reporter.reporter_agent import ReporterAgent
from pubmed_pipeline.agents.rag_answer.rag_answer_agent import RAGAnswerAgent


class AgentState(BaseModel):
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query: str = ""
    intent: Optional[str] = None

    summaries: Optional[str] = None
    insights: Optional[List[str]] = None
    final_answer: Optional[str] = None

    retrieved_docs: Optional[List[dict]] = None
    execution_order: List[str] = Field(default_factory=list)
    used_llm: Optional[bool] = None


def build_graph():
    """
    Build the 4-node LangGraph pipeline:

        router → summarizer → reporter → rag_answer
    """
    graph = StateGraph(AgentState)

    graph.add_node("router", RouterAgent())
    graph.add_node("summarizer", SummarizerAgent())
    graph.add_node("reporter", ReporterAgent())
    graph.add_node("rag_answer", RAGAnswerAgent())

    graph.set_entry_point("router")
    graph.add_edge("router", "summarizer")
    graph.add_edge("summarizer", "reporter")
    graph.add_edge("reporter", "rag_answer")
    graph.set_finish_point("rag_answer")

    return graph.compile()
