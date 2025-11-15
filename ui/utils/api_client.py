import requests

API_BASE_URL = "https://pubmed-api.delightfulbeach-6e28760e.westus.azurecontainerapps.io"

def rag_chat(question: str):
    url = f"{API_BASE_URL}/api/ask"
    payload = {"query": question}
    try:
        r = requests.post(url, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as ex:
        return {"error": str(ex)}

def document_search(query: str):
    url = f"{API_BASE_URL}/api/ask"
    payload = {"query": query}
    try:
        r = requests.post(url, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as ex:
        return {"error": str(ex)}

def agent_trace(query: str):
    url = f"{API_BASE_URL}/api/ask"
    payload = {"query": query}
    try:
        r = requests.post(url, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as ex:
        return {"error": str(ex)}
