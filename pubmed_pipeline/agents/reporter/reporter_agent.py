"""
reporter_agent.py
Generates basic high-level insights (fallback mode).
"""

from __future__ import annotations
from pubmed_pipeline.agents.base.shared import logger, mark_node_start, mark_node_end


class ReporterAgent:

    def run(self, state: dict) -> dict:
        node = "reporter"
        mark_node_start(state, node)

        query = state.get("query")
        logger.info("ReporterAgent: start")

        # Fallback insights
        insights = [
            "High-level topic identified.",
            "Primary question relates to clinical outcomes."
        ]

        logger.warning("ReporterAgent: no LLM provided; generating fallback insights.")
        state["insights"] = insights

        mark_node_end(state, node)
        return state
