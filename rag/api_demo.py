from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pubmed_pipeline.rag.rag_retriever import retrieve_docs
from pubmed_pipeline.rag.rag_generator import generate_answer
from pubmed_pipeline.utils.log_config import get_logger
import uvicorn
import time

# ---------------------------------------------------------------------------
# FastAPI App – INNVO-491 (RAG Pipeline Endpoint)
# ---------------------------------------------------------------------------

app = FastAPI(title="PubMed RAG Pipeline API", version="5.0.0")
logger = get_logger(__name__)

@app.get("/rag/query")
def rag_query_endpoint(query: str = Query(..., description="User query text"),
                       top_k: int = Query(3, description="Number of docs to retrieve")):
    """
    REST endpoint combining retriever + generator.
    Example:
      GET /rag/query?query=cisplatin%20S-1%20gastric%20cancer%20outcomes&top_k=3
    """
    start_time = time.time()
    logger.info(f"🔍 Received RAG query: '{query}' (top_k={top_k})")

    try:
        # 1️⃣ Retrieve context docs
        docs = retrieve_docs(query, top_k=top_k)
        logger.info(f"📄 Retrieved {len(docs)} candidate documents for generation.")

        # 2️⃣ Generate final answer
        result = generate_answer(query, docs)
        elapsed = round((time.time() - start_time) * 1000, 2)
        logger.info(f"✅ RAG pipeline completed in {elapsed} ms.")

        return JSONResponse(content={
            "query": query,
            "docs_retrieved": len(docs),
            "result": result,
            "latency_ms": elapsed
        })

    except Exception as e:
        logger.error(f"❌ RAG pipeline failed: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"error": str(e)})


# ---------------------------------------------------------------------------
# CLI launch:  python3 -m pubmed_pipeline.rag.api_demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    logger.info("🚀 Starting FastAPI RAG server at http://127.0.0.1:8000/rag/query")
    uvicorn.run("pubmed_pipeline.rag.api_demo:app", host="127.0.0.1", port=8000, reload=False)
