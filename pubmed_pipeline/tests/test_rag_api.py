# ============================================================
# 🧪 FastAPI Endpoint Tests — INNVO-491
# ------------------------------------------------------------
# Run with: python3 -m pytest -v pubmed_pipeline/tests/test_rag_api.py
# ============================================================

import pytest
from fastapi.testclient import TestClient
from pubmed_pipeline.rag.api_demo import app

client = TestClient(app)

def test_root_endpoint():
    r = client.get("/")
    assert r.status_code == 200
    assert "PubMed RAG API" not in r.text  # sanity check message only
    assert "/rag/query" in r.json()["endpoints"]

def test_rag_query_endpoint(monkeypatch):
    # mock pipeline
    from pubmed_pipeline.rag import rag_pipeline_demo
    monkeypatch.setattr(rag_pipeline_demo, "run_rag_pipeline",
                        lambda q, top_k=5: {"query": q, "answer": "mock answer", "sources": ["mock"], "num_docs": 1, "latency_sec": 0.1})

    payload = {"query": "cisplatin S-1 gastric cancer outcomes", "top_k": 3}
    r = client.post("/rag/query", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "answer" in data and "sources" in data and "latency_sec" in data
