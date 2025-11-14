import requests

API_BASE = "http://pubmed-api:8000"  # Update when backend is deployed

def query_rag(question: str):
    url = f"{API_BASE}/rag/query"
    payload = {"query": question}
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        return {"error": response.text}
    return response.json()

def search_documents(term: str):
    url = f"{API_BASE}/documents/search"
    params = {"query": term}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return {"error": response.text}
    return response.json()
