# pubmed_pipeline/agents/base/langgraph_env.py

"""
LangGraph Execution Environment

This module provides the single public function:

    run_graph(query: str, top_k: int = 5) -> AgentState

FastAPI uses this to execute the multi-agent PubMed pipeline.
"""

from uuid import uuid4
from typing import Any, Dict

from pubmed_pipeline.agents.base.shared import AgentState
from pubmed_pipeline.agents.base.dag_controller import build_agent_graph


def run_graph(query: str, top_k: int = 5) -> AgentState:
    """
    Executes the PubMed LangGraph DAG end-to-end.

    Parameters
    ----------
    query : str
        User question.
    top_k : int
        Number of vector search documents to retrieve.

    Returns
    -------
    AgentState
        Final pipeline state after all agents run.
    """

    # Unique trace for logs + UI
    trace_id = str(uuid4())

    # Minimal clean initial state — all other attributes have defaults
    initial_state = AgentState(
        trace_id=trace_id,
        query=query,
        intent="answer",
    )

    # Build the DAG
    graph = build_agent_graph()

    # Runtime config for nodes
    config: Dict[str, Any] = {
        "configurable": {
            "top_k": top_k,
            "trace_id": trace_id,
        }
    }

    # Execute pipeline
    final_state = graph.invoke(initial_state, config=config)

    return final_state
