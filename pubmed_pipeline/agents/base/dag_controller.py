"""
dag_controller.py
Controls the LangGraph pipeline execution and artifact saving.
"""

from __future__ import annotations

import time
import uuid
from typing import Any, Dict

from langgraph.graph import StateGraph, END

from pubmed_pipeline.agents.base.shared import logger
from pubmed_pipeline.agents.router.router_agent import RouterAgent
from pubmed_pipeline.agents.summarizer.summarizer_agent import SummarizerAgent
from pubmed_pipeline.agents.reporter.reporter_agent import ReporterAgent
from pubmed_pipeline.agents.rag_answer.rag_answer_agent import RAGAnswerAgent

from pubmed_pipeline.utils.artifact_writer import ArtifactWriter


class DAGController:
    def __init__(self):
        self.app = None
        logger.info("DAGController initialized")

    # ------------------------------------------------------------
    # Build graph
    # ------------------------------------------------------------
    def _build_graph(self):
        logger.info("Compiling LangGraph pipeline...")

        workflow = StateGraph(dict)

        workflow.add_node("router", RouterAgent().run)
        workflow.add_node("summarizer", SummarizerAgent().run)
        workflow.add_node("reporter", ReporterAgent().run)
        workflow.add_node("rag_answer", RAGAnswerAgent().run)

        workflow.set_entry_point("router")
        workflow.add_edge("router", "summarizer")
        workflow.add_edge("summarizer", "reporter")
        workflow.add_edge("reporter", "rag_answer")
        workflow.add_edge("rag_answer", END)

        self.app = workflow.compile()
        logger.info("LangGraph pipeline compiled successfully.")

    # ------------------------------------------------------------
    # Run graph
    # ------------------------------------------------------------
    def run(self, query: str, debug: bool = True) -> Dict[str, Any]:
        if self.app is None:
            self._build_graph()

        trace_id = str(uuid.uuid4())
        logger.info(f"Starting DAG run trace_id={trace_id}")

        start = time.time()
        state = {"query": query, "trace_id": trace_id}

        final_state = self.app.invoke(state)

        runtime = time.time() - start

        # Extract result
        result = {
            "summary": final_state.get("summary"),
            "insights": final_state.get("insights"),
            "retrieved_docs": final_state.get("retrieved_docs"),
            "final_answer": final_state.get("final_answer"),
        }

        metadata = {
            "node_sequence": final_state.get("node_sequence", []),
            "timestamps": final_state.get("timestamps", {}),
            "runtime_seconds": runtime,
        }

        # Save artifacts
        writer = ArtifactWriter(trace_id)
        artifact_paths = writer.save_all(
            summary=result.get("summary"),
            insights=result.get("insights"),
            retrieved_docs=result.get("retrieved_docs"),
            final_answer=result.get("final_answer"),
            state=final_state,
            metadata=metadata,
        )

        response = {
            "trace_id": trace_id,
            "result": result,
            "metadata": metadata,
            "artifacts": artifact_paths,
        }

        if debug:
            response["debug"] = {"raw_state": final_state}

        logger.info(
            f"DAG completed trace_id={trace_id} runtime={runtime:.3f}s"
        )
        return response


if __name__ == "__main__":
    controller = DAGController()
    out = controller.run("Does cisplatin plus S-1 improve gastric cancer outcomes?")
    logger.info("DAGController response: %s", out)
