import requests
from typing import Any, Dict, Optional

# -------------------------------------------------------------------
# Azure FastAPI backend public endpoint
# Replace with your actual FQDN if different
# -------------------------------------------------------------------
API_BASE_URL = "https://pubmed-api.delightfulbeach-6e28760e.westus.azurecontainerapps.io"


# -------------------------------------------------------------------
# Internal helper – unified HTTP request handler
# -------------------------------------------------------------------
def _request(method: str, url: str, *, json: Optional[dict] = None, timeout: int = 60):
    """
    Generic request wrapper with consistent error handling.

    Parameters
    ----------
    method : str
        HTTP method ("GET", "POST")
    url : str
        Full request URL
    json : dict, optional
        JSON body for POST requests
    timeout : int
        Timeout in seconds

    Returns
    -------
    Any
        Parsed JSON response

    Raises
    ------
    RuntimeError
        On connection issues, non-200 responses, or invalid JSON.
    """
    try:
        response = requests.request(method, url, json=json, timeout=timeout)
    except requests.RequestException as exc:
        raise RuntimeError(f"API request error: {exc}") from exc

    if response.status_code != 200:
        raise RuntimeError(
            f"API returned {response.status_code}: {response.text}"
        )

    try:
        return response.json()
    except ValueError as exc:
        raise RuntimeError(f"Failed to parse JSON: {response.text}") from exc


# -------------------------------------------------------------------
# /api/ask – RAG pipeline
# -------------------------------------------------------------------
def query_rag(question: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Call the RAG pipeline.

    Parameters
    ----------
    question : str
        User's biomedical question.
    top_k : int
        Number of documents to retrieve.

    Returns
    -------
    dict
        Parsed RAG pipeline response.
    """
    url = f"{API_BASE_URL}/api/ask"
    payload = {"query": question, "top_k": top_k}
    return _request("POST", url, json=payload)


# -------------------------------------------------------------------
# /api/trace/{trace_id} – Retrieve LangGraph agent trace
# -------------------------------------------------------------------
def get_trace(trace_id: str) -> Dict[str, Any]:
    """
    Fetch the full execution trace for a given pipeline run.

    Parameters
    ----------
    trace_id : str
        Unique ID returned by the RAG pipeline.

    Returns
    -------
    dict
        The execution trace.
    """
    url = f"{API_BASE_URL}/api/trace/{trace_id}"
    return _request("GET", url)
