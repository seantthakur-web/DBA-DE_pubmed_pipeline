"""
router_agent.py
Simple routing agent for LangGraph pipeline.
Determines which pipeline branch to follow (fixed branch for now).
"""

from __future__ import annotations
from pubmed_pipeline.agents.base.shared import logger, mark_node_start, mark_node_end


class RouterAgent:

    def run(self, state: dict) -> dict:
        node = "router"
        mark_node_start(state, node)

        query = state.get("query")
        logger.info("RouterAgent: routing query=%r", query)

        # Always send to RAG pipeline (single-path design for Sprint 6)
        state["route"] = "rag_pipeline"

        mark_node_end(state, node)
        return state
