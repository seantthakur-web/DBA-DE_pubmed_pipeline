from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field
from typing import List, Optional

# Import agent nodes
from pubmed_pipeline.agents.router.router_agent import router_node
from pubmed_pipeline.agents.summarizer.summarizer_agent import summarizer_node
from pubmed_pipeline.agents.reporter.reporter_agent import reporter_node
from pubmed_pipeline.agents.rag_answer.rag_answer_agent import rag_answer_node


# ======================================================
# Shared Agent State
# ======================================================

class AgentState(BaseModel):
    trace_id: str
    query: str
    intent: Optional[str] = None
    summaries: Optional[List[str]] = None
    insights: Optional[List[str]] = None
    retrieved_docs: Optional[List[dict]] = None
    final_answer: Optional[str] = None
    used_llm: bool = False
    execution_order: List[str] = Field(default_factory=list)


# ======================================================
# DAG Builder
# ======================================================

def build_agent_graph():
    """
    Production DAG for INNVO-501.
    Execution path:
        router → summarizer → reporter → rag_answer → END
    """

    graph = StateGraph(AgentState)

    # Register nodes
    graph.add_node("router", router_node)
    graph.add_node("summarizer", summarizer_node)
    graph.add_node("reporter", reporter_node)
    graph.add_node("rag_answer", rag_answer_node)

    # Wire DAG edges
    graph.add_edge("router", "summarizer")
    graph.add_edge("summarizer", "reporter")
    graph.add_edge("reporter", "rag_answer")
    graph.add_edge("rag_answer", END)

    # Set entry point
    graph.set_entry_point("router")

    # Compile graph
    return graph.compile()
