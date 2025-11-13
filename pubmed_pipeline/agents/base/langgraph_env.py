"""
langgraph_env.py
Full LangGraph pipeline runner (fallback mode).
Router → Summarizer → Reporter → RAGAnswer → END
"""

from __future__ import annotations

import uuid
import time

from langgraph.graph import StateGraph, END

# Shared state
from pubmed_pipeline.agents.base.shared import AgentState

# Agents
from pubmed_pipeline.agents.router.router_agent import RouterAgent
from pubmed_pipeline.agents.summarizer.summarizer_agent import SummarizerAgent
from pubmed_pipeline.agents.reporter.reporter_agent import ReporterAgent
from pubmed_pipeline.agents.rag_answer.rag_answer_agent import RAGAnswerAgent

# Logging
from pubmed_pipeline.utils.log_config import get_logger

logger = get_logger(__name__)


# --------------------------------------------------------------------
# Metadata wrapper (injects trace_id, timestamps, node order)
# --------------------------------------------------------------------
def wrap_with_metadata(agent_name, func):
    def wrapped(state: AgentState) -> AgentState:
        # Generate trace_id if first node
        if not state.trace_id:
            state.trace_id = str(uuid.uuid4())

        trace_id = state.trace_id
        logger.info(f"[trace_id={trace_id}] → Starting node: {agent_name}")

        # Timestamp start
        state.timestamps[f"{agent_name}_start"] = time.time()

        # Add node name to sequence
        state.node_sequence.append(agent_name)

        # Execute agent
        result = func(state)

        # Timestamp end
        state.timestamps[f"{agent_name}_end"] = time.time()

        logger.info(f"[trace_id={trace_id}] ← Completed node: {agent_name}")

        return result

    return wrapped


# --------------------------------------------------------------------
# Build LangGraph pipeline (fallback — no LLM)
# --------------------------------------------------------------------
def build_graph():
    logger.warning("LangGraph running in fallback mode (no LLM).")

    llm = None  # Deterministic fallback for all agents

    router_agent = RouterAgent(llm=llm)
    summarizer_agent = SummarizerAgent(llm=llm)
    reporter_agent = ReporterAgent(llm=llm)
    rag_answer_agent = RAGAnswerAgent(llm=llm)

    graph = StateGraph(AgentState)

    graph.add_node("router", wrap_with_metadata("router", router_agent.run))
    graph.add_node("summarizer", wrap_with_metadata("summarizer", summarizer_agent.run))
    graph.add_node("reporter", wrap_with_metadata("reporter", reporter_agent.run))
    graph.add_node("rag_answer", wrap_with_metadata("rag_answer", rag_answer_agent.run))

    # Pipeline ordering
    graph.set_entry_point("router")
    graph.add_edge("router", "summarizer")
    graph.add_edge("summarizer", "reporter")
    graph.add_edge("reporter", "rag_answer")
    graph.add_edge("rag_answer", END)

    logger.info("LangGraph pipeline constructed successfully.")

    return graph.compile()


# --------------------------------------------------------------------
# Smoke test entry point
# --------------------------------------------------------------------
if __name__ == "__main__":
    logger.info("🚀 Starting LangGraph Smoke Test (fallback mode)")

    app = build_graph()

    query = "Does cisplatin plus S-1 improve gastric cancer outcomes?"
    initial_state = AgentState(query=query)

    # Final output is returned as a dict, not AgentState
    final_state = app.invoke(initial_state)

    logger.info("========================================")
    logger.info("LangGraph Pipeline Completed Successfully")

    logger.info("Trace ID: %s", final_state.get("trace_id"))
    logger.info("Execution Order: %s", final_state.get("node_sequence"))

    logger.info("\n--- Summary ---\n%s", final_state.get("summary"))
    logger.info("\n--- Insights ---\n%s", final_state.get("insights"))
    logger.info("\n--- Retrieved Docs ---\n%s", final_state.get("retrieved_docs"))
    logger.info("\n--- Final Answer ---\n%s", final_state.get("final_answer"))

    logger.info("========================================")
