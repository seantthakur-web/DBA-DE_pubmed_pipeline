"""
summarizer_agent.py
Produces a lightweight summary of the user query (fallback mode).
"""

from __future__ import annotations
from pubmed_pipeline.agents.base.shared import logger, mark_node_start, mark_node_end


class SummarizerAgent:

    def run(self, state: dict) -> dict:
        node = "summarizer"
        mark_node_start(state, node)

        query = state.get("query")

        if not query:
            summary = "No query provided."
            logger.warning("SummarizerAgent: missing query; using fallback summary.")
        else:
            summary = f"This query asks about: {query[:80]}..."

        logger.info("SummarizerAgent: completed")
        state["summary"] = summary

        mark_node_end(state, node)
        return state
