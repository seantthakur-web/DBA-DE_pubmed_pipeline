import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from pubmed_pipeline.utils.log_config import get_logger

logger = get_logger(__name__)

# ======================================================
# Explicit .env load
# ======================================================

ENV_PATH = "/home/seanthakur/pubmed_pipeline/.env"
if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)
    logger.info(f"Loaded .env from {ENV_PATH}")
else:
    logger.error(f".env file not found at {ENV_PATH}")


# ======================================================
# Internal Azure OpenAI client builder
# ======================================================

def _get_base_client():
    """
    Loads Azure OpenAI credentials (key, endpoint, api_version)
    and returns an AzureOpenAI client.
    """
    key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")

    if not key or not endpoint or not api_version:
        logger.error("Missing Azure OpenAI credentials.")
        raise ValueError(
            "Missing Azure OpenAI credentials "
            "(AZURE_OPENAI_API_KEY / AZURE_OPENAI_ENDPOINT / AZURE_OPENAI_API_VERSION)."
        )

    logger.info("Initializing Azure OpenAI client.")
    client = AzureOpenAI(
        api_key=key,
        api_version=api_version,
        azure_endpoint=endpoint
    )
    return client


# ======================================================
# Chat Model Loader
# ======================================================

def get_client_and_chat_model():
    """
    Returns (client, deployment_name) for chat/LLM.
    """
    model = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
    client = _get_base_client()
    return client, model


# ======================================================
# Embedding Model Loader
# ======================================================

def get_client_and_embed_model():
    """
    Returns (client, deployment_name) for embeddings.
    """
    model = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002")
    client = _get_base_client()
    return client, model


# ======================================================
# Chat completion wrapper
# ======================================================

def chat_completion(messages: list):
    """
    Send messages to Azure OpenAI chat/LLM.
    """
    client, model = get_client_and_chat_model()

    try:
        logger.info(f"Calling Azure Chat LLM | deployment={model}")
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2,
        )
        return response.choices[0].message["content"]

    except Exception as e:
        logger.error(f"Azure Chat LLM failed: {e}")
        raise


# ======================================================
# Embedding wrapper
# ======================================================

def embed_text(text: str):
    """
    Create embeddings using Azure OpenAI deployment.
    """
    client, model = get_client_and_embed_model()

    logger.info(f"Embedding text using Azure OpenAI | deployment={model}")

    try:
        response = client.embeddings.create(
            model=model,   # MUST MATCH DEPLOYMENT NAME
            input=text
        )
        embedding = response.data[0].embedding
        return embedding

    except Exception as e:
        logger.error(f"Azure OpenAI embedding failed: {e}")
        raise
