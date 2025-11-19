import logging
from utils.keyvault_client import get_secret
from utils.log_config import get_logger
from rag.rag_retriever import retrieve_docs

logger = get_logger(__name__)


def generate_answer(query: str, docs):
    """
    Simple RAG answer generator.
    Replace this with Azure OpenAI integration.
    """
    if not docs:
        return "No documents retrieved — cannot generate answer."

    # Placeholder logic for Sprint 6
    context_texts = "\n".join([d.get("text", "") for d in docs])

    answer = f"Answer based on retrieved documents:\n\n{context_texts}"
    return answer
