# ============================================================
# 🔁 RAG Pipeline Orchestrator — INNVO-491
# ------------------------------------------------------------
# Chains retriever → generator into one callable function.
# Used by FastAPI endpoint and CLI.
# ============================================================

import time
import logging
from pubmed_pipeline.rag import rag_retriever, rag_generator
from pubmed_pipeline.utils.log_config import setup_logger

logger = setup_logger(__name__)

def run_rag_pipeline(query: str, top_k: int = 5):
    """
    Executes the full RAG flow: retrieval → generation.
    """
    start = time.time()
    logger.info(f"🚀 Starting RAG pipeline for query: {query}")

    # Step 1: Retrieve top-K docs
    retrieved_docs = rag_retriever.retrieve_docs(query, top_k=top_k)
    logger.info(f"📚 Retrieved {len(retrieved_docs)} docs")

    # Step 2: Generate grounded summary
    result = rag_generator.generate_answer(query, retrieved_docs, top_k=top_k)

    latency = round(time.time() - start, 2)
    result["latency_sec"] = latency

    logger.info(f"✅ Completed RAG pipeline | latency={latency}s")
    return result

# ------------------------------------------------------------
# CLI Test
# ------------------------------------------------------------
if __name__ == "__main__":
    sample_query = "cisplatin S-1 gastric cancer outcomes"
    print(run_rag_pipeline(sample_query))
