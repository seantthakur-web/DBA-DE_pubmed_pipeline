"""
LangGraph Environment Setup
---------------------------
Router → Summarizer → Reporter → END
"""

import uuid
from agents.base.shared import AgentState, logger
from agents.summarizer.summarizer_agent import summarizer_node
from agents.reporter.reporter_agent import reporter_node


# ============================================================
# ROUTER NODE
# ============================================================

def router_node(state: AgentState) -> dict:
    """Router only logs and returns empty update."""
    logger.info(
        f"Router node invoked | trace_id={state.trace_id} | query={state.query}"
    )
    return {}   # ✔ return an empty dict update


# ============================================================
# GRAPH BUILDER
# ============================================================

def build_graph():
    from langgraph.graph import StateGraph, END

    graph = StateGraph(AgentState)

    graph.add_node("router", router_node)
    graph.add_node("summarizer", summarizer_node)
    graph.add_node("reporter", reporter_node)

    graph.set_entry_point("router")
    graph.add_edge("router", "summarizer")
    graph.add_edge("summarizer", "reporter")
    graph.add_edge("reporter", END)

    logger.info("LangGraph compiled: router → summarizer → reporter → END")
    return graph.compile()


# ============================================================
# SMOKE TEST
# ============================================================

def run_smoke_test():
    logger.info("Starting LangGraph smoke test")

    graph = build_graph()

    test_state = AgentState(
        query="test query for reporter flow",
        trace_id=str(uuid.uuid4()),
        documents=[],
        summary="",
        insights="",
        answer="",
        metadata={},
        debug={},
    ).model_dump()

    result = graph.invoke(test_state)

    logger.info(
        f"Smoke test completed | trace_id={result.get('trace_id')} | keys={list(result.keys())}"
    )
    logger.info("LangGraph environment smoke test passed")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    run_smoke_test()
