import logging
from utils.keyvault_client import get_secret
from utils.log_config import get_logger

logger = get_logger("rag_retriever")


def retrieve_docs(query: str, top_k: int = 3):
    """
    Dummy pgvector retriever for Sprint 6.
    Replace with actual PostgreSQL pgvector retrieval.
    """
    logger.info(f"Retrieving top {top_k} results for query: '{query}'")

    # Mock documents for now
    return [
        {"text": f"Mock retrieved document for: {query} (1/{top_k})"},
        {"text": f"Mock retrieved document for: {query} (2/{top_k})"},
        {"text": f"Mock retrieved document for: {query} (3/{top_k})"},
    ]
