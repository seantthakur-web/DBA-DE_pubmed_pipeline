# 🧬 PubMed + OrderPipeline Project

### **v6.0.0 – LangGraph Agents + FastAPI Service + Artifact System (Azure Production Build)**

This release transforms the PubMed Pipeline from a standalone RAG demo into a **fully agentic biomedical AI service** deployed on an **Azure VM** with:

* LangGraph multi-agent DAG
* FastAPI backend
* pgvector retrieval
* Azure OpenAI (embeddings + LLM)
* Caddy reverse proxy for external access
* Full artifact logging for every request
* Packaged Python module (`pip install -e .`)

It is now a **cloud-served biomedical question-answering system** with reproducible trace artifacts and a modular agent architecture.

---

# 📘 Overview

The PubMed Knowledge Graph + OrderPipeline system has gone through **six structured sprints**, evolving from raw ETL extraction into a fully orchestrated agentic RAG service.

### **This v6.0 milestone delivers:**

* A **four-node LangGraph DAG**:
  `router → summarizer → reporter → rag_answer`
* The **DAGController**, a production orchestrator managing execution, caching, and trace IDs
* A **FastAPI backend** exposing a public RAG endpoint
* A complete **artifact system** generating reproducible logs per run
* Updated **pgvector ingestion pipeline** for 225 PubMed abstracts
* **Caddy reverse proxy** exposing public HTTP access
* **Packaged Python module** with fully stable import paths

---

# 🎯 Core Architecture (v6.0)

### **Request Flow**

```
User Query
    ↓
FastAPI (/rag/query)
    ↓
DAGController (trace_id generated)
    ↓
LangGraph DAG
    • router
    • summarizer
    • reporter
    • rag_answer
    ↓
ArtifactWriter → data/artifacts/<trace_id>/
    ↓
FastAPI JSON Response
```

### **Produced Artifacts (per request)**

Located at: `pubmed_pipeline/data/artifacts/<trace_id>/`

```
final_answer.txt
retrieved_docs.json
summary.txt
insights.json
state.json
metadata.json
```

---

# 🧭 Sprint Progress Overview

| Sprint | Dates           | Focus Area                    | Status                   |
| ------ | --------------- | ----------------------------- | ------------------------ |
| 1      | Oct 8 – Oct 21  | Foundations / ETL             | ✅ Completed              |
| 2      | Oct 22 – Nov 7  | Azure Migration               | ✅ Completed              |
| 3      | Nov 8 – Nov 18  | Integration Live              | ✅ Completed              |
| 4      | Nov 19 – Dec 2  | AI Layer (Semantic Retrieval) | ✅ Completed              |
| 5      | Dec 3 – Dec 16  | RAG Finalization              | ✅ Completed              |
| 6      | Dec 17 – Dec 31 | LangGraph + API Service       | **✅ Completed (v6.0.0)** |

---

# 🚀 What’s New in v6.0.0

## **1. Full LangGraph Multi-Agent Pipeline**

Agents implemented and integrated:

* **RouterAgent** – classifies query intent
* **SummarizerAgent** – condenses retrieved evidence
* **ReporterAgent** – extracts structured insights
* **RAGAnswerAgent** – final biomedical answer generation

Includes full deterministic DAG and smoke tests.

---

## **2. DAGController (Production Orchestrator)**

Core responsibilities:

* Builds and caches a single LangGraph instance
* Generates UUID trace IDs
* Writes artifacts
* Executes end-to-end runs via `run_pipeline()`
* Returns structured response objects

Entry point:
`pubmed_pipeline/agents/base/dag_controller.py`

---

## **3. ArtifactWriter System**

Every request creates:

```
pubmed_pipeline/data/artifacts/<trace_id>/
    final_answer.txt
    summary.txt
    insights.json
    retrieved_docs.json
    metadata.json
    state.json
```

This enables:

* Auditing
* Reproducibility
* Trace-correctness
* Debugging & ML observability

---

## **4. FastAPI Production Backend**

### Endpoints:

| Method | Route        | Purpose                   |
| ------ | ------------ | ------------------------- |
| POST   | `/rag/query` | Main agentic RAG endpoint |
| GET    | `/health`    | Health check              |
| GET    | `/docs`      | Swagger UI                |

Module:
`pubmed_pipeline/api/main.py`

FastAPI uses the DAGController internally.

---

## **5. Caddy Reverse Proxy (Azure VM)**

`/etc/caddy/Caddyfile`:

```
http://4.246.99.209 {
    reverse_proxy 127.0.0.1:8000
}
```

This exposes **public HTTP** without modifying Uvicorn.

### Public Swagger UI:

**[http://4.246.99.209/docs](http://4.246.99.209/docs)**

---

## **6. Python Packaging (pip install -e .)**

You can now run:

```bash
pip install -e .
```

Imports are now clean:

```
from pubmed_pipeline.agents.router.router_agent import RouterAgent
from pubmed_pipeline.api.main import app
```

---

# 🌐 Deployment Status (Azure VM)

| Component           | Status | Notes                                                |
| ------------------- | ------ | ---------------------------------------------------- |
| Azure VM            | ✅      | Ubuntu 22.04, Python 3.12                            |
| FastAPI (Uvicorn)   | ✅      | Running 0.0.0.0:8000                                 |
| Caddy Reverse Proxy | ✅      | Public endpoint                                      |
| Swagger UI          | ✅      | [http://4.246.99.209/docs](http://4.246.99.209/docs) |
| LangGraph DAG       | ✅      | All nodes integrated                                 |
| ArtifactWriter      | ✅      | Producing per-trace folders                          |
| pgvector ingestion  | ✅      | ~900 chunks from 225 abstracts                       |

---

# 🧪 Validation Checklist (v6.0)

### **1. LangGraph Smoke Test**

```bash
python3 -m pubmed_pipeline.agents.base.dag_controller
```

Expected:

* Router ✔
* Summarizer ✔
* Reporter ✔
* RAG_Answer ✔
* Artifacts folder created ✔

---

### **2. FastAPI**

```bash
curl http://127.0.0.1:8000/health
```

---

### **3. Public Endpoint**

From any device/browser:

```
http://4.246.99.209/docs
```

---

### **4. RAG Query Example**

```bash
curl -X POST "http://4.246.99.209/rag/query" \
  -H "Content-Type: application/json" \
  -d '{"query":"cisplatin S-1 gastric cancer outcomes", "top_k": 3}'
```

---

# 📁 Updated Directory Structure (After Packaging)

```
pubmed_pipeline/
│
├── pubmed_pipeline/
│   ├── agents/
│   │   ├── base/
│   │   │   ├── shared.py
│   │   │   ├── dag_controller.py
│   │   ├── router/
│   │   ├── summarizer/
│   │   ├── reporter/
│   │   ├── rag_answer/
│   │
│   ├── api/
│   │   ├── main.py
│   │   ├── routes/
│   │   │   └── rag_endpoint.py
│   │   └── schemas.py
│   │
│   ├── rag/
│   │   ├── rag_retriever.py
│   │   ├── ingest_chunks_to_pg.py
│   │
│   ├── data/
│   │   ├── artifacts/
│   │   ├── storage/
│   │
│   ├── utils/
│   │   ├── log_config.py
│   │   ├── keyvault_client.py
│   │   ├── artifact_writer.py
│   │
│   ├── etl/
│   │   ├── rebuild_papers_from_pubmed_query.py
│   │
│   └── __init__.py
│
├── setup.py
├── README.md
├── requirements.txt
└── venv/
```

---

# 🧠 Key Modules

### **DAGController**

Core orchestrator for agent runs:
`pubmed_pipeline/agents/base/dag_controller.py`

### **ArtifactWriter**

Trace-level I/O:
`pubmed_pipeline/utils/artifact_writer.py`

### **FastAPI Backend**

`pubmed_pipeline/api/main.py`

### **LangGraph DAG**

Defined in the **Controller**, not spread across files.

---

# 📝 Release Notes — v6.0.0

### **Added**

* Full 4-node LangGraph pipeline
* DAGController orchestration engine
* ArtifactWriter subsystem
* FastAPI production backend
* Public Swagger UI (Caddy reverse proxy)
* Editable Python module packaging
* Rebuilt pgvector ingestion pipeline for 225 abstracts

### **Improved**

* Logging (structured + timestamps)
* Error traceability
* Import path stability
* Modular architecture

### **Removed**

* Old test scripts
* Experimental entrypoints
* Duplicate agent wrappers

---

# 👤 Maintainer

**Sean Thakur**
Azure VM: `pubmed-dev-vm` (West US)
Project Repo: `github.com/seantthakur-web/DBA-DE_pubmed_pipeline`
Last Updated: **Nov 15, 2025**


