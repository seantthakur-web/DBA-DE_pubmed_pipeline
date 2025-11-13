"""
rag_answer_agent.py
Uses mock retrieval + deterministic fallback answer for Sprint 6.
"""

from __future__ import annotations
from pubmed_pipeline.agents.base.shared import logger, mark_node_start, mark_node_end


class RAGAnswerAgent:

    def run(self, state: dict) -> dict:
        node = "rag_answer"
        mark_node_start(state, node)

        query = state.get("query")
        logger.info("RAGAnswerAgent: starting run for trace_id=%s", state.get("trace_id"))
        logger.info("RAGAnswerAgent: using structured mock retrieval for query=%r", query)

        # Mock retrieval
        retrieved_docs = [
            {
                "id": "MOCK_PMID_0001",
                "text": "Cisplatin and S-1 combination therapy has shown improved overall survival in advanced gastric cancer.",
                "score": 0.92,
            },
            {
                "id": "MOCK_PMID_0002",
                "text": "Fluorouracil-based regimens remain a standard backbone in gastroesophageal adenocarcinoma treatment.",
                "score": 0.88,
            },
        ]

        state["retrieved_docs"] = retrieved_docs

        # Deterministic fallback final answer
        logger.warning("RAGAnswerAgent: no LLM configured; using deterministic fallback answer.")

        summary = state.get("summary", "")
        insights = state.get("insights", [])

        final_answer = f"""Based on the available mock evidence, here is a synthesized answer to your question:

Question: {query}

Summary: {summary}

Key insights:
- {insights[0]}
- {insights[1]}

Supporting documents:
- {retrieved_docs[0]["text"]}
- {retrieved_docs[1]["text"]}
"""

        state["final_answer"] = final_answer

        logger.info("RAGAnswerAgent: completed run for trace_id=%s", state.get("trace_id"))

        mark_node_end(state, node)
        return state
