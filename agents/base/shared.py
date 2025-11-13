"""
Shared utilities for LangGraph agents.
Contains:
- AgentState (pydantic model)
- logger
- load_prompt()
- build_azure_llm()
"""

import os
from pydantic import BaseModel, Field
from utils.log_config import get_logger

logger = get_logger("agents.shared")


# --------------------------------------------------------------------------------------
# AgentState (Pydantic Model)
# --------------------------------------------------------------------------------------
class AgentState(BaseModel):
    """Unified state object passed between LangGraph nodes."""

    query: str = Field(default="", description="User query")
    documents: list[str] = Field(default_factory=list)
    summary: str = Field(default="")
    insights: str = Field(default="")
    answer: str = Field(default="")
    metadata: dict = Field(default_factory=dict)
    trace_id: str = Field(default="")
    debug: dict = Field(default_factory=dict)


# --------------------------------------------------------------------------------------
# Utility: Load a prompt template from file
# --------------------------------------------------------------------------------------
def load_prompt(path: str, default_text: str) -> str:
    """Loads a text file; if missing, returns default text."""
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return f.read()
        except Exception as e:
            logger.warning(f"Failed to load prompt at {path}: {e}")

    logger.warning(f"Prompt template missing, using fallback for {path}")
    return default_text


# --------------------------------------------------------------------------------------
# Utility: Azure OpenAI model loader
# --------------------------------------------------------------------------------------
def build_azure_llm(mode: str = "summary"):
    """
    Returns AzureChatOpenAI instance for:
    - "summary"
    - "insight"

    Returns None if Azure config missing.
    """
    try:
        from langchain_openai import AzureChatOpenAI

        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        api_key = os.getenv("AZURE_OPENAI_API_KEY", "")
        deployment = "gpt-4o-mini"  # same model for both for now

        if not endpoint or not api_key:
            raise ValueError("Azure OpenAI configuration missing.")

        model = AzureChatOpenAI(
            azure_endpoint=endpoint,
            azure_deployment=deployment,
            api_key=api_key,
            api_version="2024-10-21",
            temperature=0.2,
        )

        return model

    except Exception as e:
        logger.error(f"Azure LLM init failed: {e}")
        return None
