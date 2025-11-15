from fastapi import APIRouter, HTTPException, Query
from pubmed_pipeline.rag.rag_retriever import retrieve_docs
from pubmed_pipeline.utils.log_config import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["rag"])


@router.get("/rag/retrieve")
async def rag_retrieve(
    query: str = Query(..., description="Free-text biomedical query"),
    top_k: int = Query(5, description="Number of docs to retrieve"),
):
    query = query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query must not be empty.")

    try:
        docs = retrieve_docs(query=query, top_k=top_k)
        return {"query": query, "top_k": top_k, "retrieved_docs": docs}
    except Exception as e:
        logger.exception(f"/rag/retrieve failed: {e}")
        raise HTTPException(status_code=500, detail="Retrieval failed.")
