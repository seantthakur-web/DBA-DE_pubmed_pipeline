import requests
from typing import Any, Dict, Optional

# -------------------------------------------------------------------
# Azure FastAPI backend public endpoint
# Replace with your actual FQDN if different
# -------------------------------------------------------------------
API_BASE_URL = "https://pubmed-api.delightfulbeach-6e28760e.westus.azurecontainerapps.io"


# -------------------------------------------------------------------
# Internal helper – unified HTTP request wrapper
# -------------------------------------------------------------------
def _request(
    method: str,
    url: str,
    *,
    json: Optional[Dict[str, Any]] = None,
    timeout: int = 60
) -> Any:
    """
    Unified HTTP request handler with consistent error handling.

    Parameters
    ----------
    method : str
        HTTP method (GET, POST, etc.).
    url : str
        Fully-qualified request URL.
    json : dict, optional
        JSON body for POST requests.
    timeout : int
        Timeout in seconds.

    Returns
    -------
    Any
        Parsed JSON response.

    Raises
    ------
    RuntimeError
        For network errors, HTTP errors, or invalid JSON.
    """
    try:
        response = requests.request(method, url, json=json, timeout=timeout)
    except requests.RequestException as exc:
        raise RuntimeError(f"API request error: {exc}") from exc

    if response.status_code != 200:
        raise RuntimeError(f"API returned {response.status_code}: {response.text}")

    try:
        return response.json()
    except ValueError as exc:
        raise RuntimeError(f"Failed to parse JSON: {response.text}") from exc


# -------------------------------------------------------------------
# /api/ask – RAG Retrieval + LangGraph pipeline
# -------------------------------------------------------------------
def query_rag(question: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Execute the RAG pipeline through the FastAPI backend.

    Parameters
    ----------
    question : str
        User's query (biomedical question).
    top_k : int
        Number of documents to retrieve via PGVector.

    Returns
    -------
    dict
        Pipeline response containing trace_id, summaries, insights,
        retrieved_docs, and final_answer.
    """
    url = f"{API_BASE_URL}/api/ask"
    payload = {"query": question, "top_k": top_k}
    return _request("POST", url, json=payload)


# -------------------------------------------------------------------
# /api/trace/{trace_id} – Retrieve LangGraph agent execution trace
# -------------------------------------------------------------------
def get_trace(trace_id: str) -> Dict[str, Any]:
    """
    Retrieve the full execution trace for a completed RAG pipeline run.

    Parameters
    ----------
    trace_id : str
        Unique ID returned by /api/ask.

    Returns
    -------
    dict
        The trace data, including intermediate states and logs.
    """
    url = f"{API_BASE_URL}/api/trace/{trace_id}"
    return _request("GET", url)
