import os
from openai import AzureOpenAI
from pubmed_pipeline.utils.log_config import get_logger

logger = get_logger(__name__)


def _get_base_client() -> AzureOpenAI:
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")

    if not api_key or not endpoint or not api_version:
        logger.error("Azure OpenAI credentials missing.")
        raise ValueError("Missing Azure OpenAI credentials (key/endpoint/version).")

    return AzureOpenAI(
        api_key=api_key,
        azure_endpoint=endpoint,
        api_version=api_version,
    )


def get_client_and_chat_model():
    """
    Returns (client, deployment_name) for chat completions.
    Usage:
        client, model = get_client_and_chat_model()
        client.chat.completions.create(model=model, messages=[...])
    """
    client = _get_base_client()
    model = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-4o")
    return client, model


def get_client_and_embed_model():
    """
    Returns (client, deployment_name) for embeddings.
    Usage:
        client, model = get_client_and_embed_model()
        client.embeddings.create(model=model, input="...")
    """
    client = _get_base_client()
    model = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002")
    return client, model
