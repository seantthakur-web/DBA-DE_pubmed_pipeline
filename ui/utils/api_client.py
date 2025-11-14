import os
import requests

# Default FastAPI URL (running in Docker / Azure)
API_URL = os.getenv("API_URL", "http://localhost:8000")

def ask_rag(query: str):
    """Calls /rag/ask endpoint."""
    payload = {"query": query}
    try:
        response = requests.post(f"{API_URL}/rag/ask", json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def search_documents(query: str):
    """Calls /rag/search endpoint."""
    try:
        response = requests.get(f"{API_URL}/rag/search", params={"q": query})
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def run_agent_trace(query: str):
    """Calls /agents/trace endpoint."""
    payload = {"query": query}
    try:
        response = requests.post(f"{API_URL}/agents/trace", json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}
