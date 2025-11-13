# 🧬 PubMed + OrderPipeline Project  
**v6.0.0 – LangGraph Agents + FastAPI Service + Artifact System**

This release marks the transition from a standalone RAG demo into a **full agentic AI service**, running on an **Azure VM**, integrated with **LangGraph**, **FastAPI**, **pgvector**, **Azure OpenAI**, and a **Caddy reverse-proxy** for secure external access.

This README has been rebuilt to reflect the new architecture and folder structure after packaging the project as a Python module (`pip install -e .`).

---

# 📘 Overview

The PubMed Knowledge Graph Pipeline has evolved through six structured sprints, progressing from ETL foundations into a fully operational **agent-based biomedical question-answering API**, backed by Azure cloud resources.

### This phase delivers:

- Full **LangGraph DAG** (router → summarizer → reporter → rag_answer)
- **DAGController** orchestrating autonomous multi-step runs
- **FastAPI backend** serving public traffic
- **Artifact system:** each request writes state, metadata, and outputs into:
pubmed_pipeline/data/artifacts/<trace_id>/

yaml
Copy code
- **Caddy reverse proxy** handling public access over HTTP  
- Public Swagger UI:  
**http://4.246.99.209/docs**

---

# 🎯 Core Architecture (v6.0)

User Query → FastAPI → DAGController → LangGraph DAG
→ Router → Summarizer → Reporter → RAG Answer Agent
→ ArtifactWriter → /data/artifacts/<trace_id>/
→ JSON response returned to FastAPI

yaml
Copy code

Components now live under:

pubmed_pipeline/
agents/
base/
shared.py
dag_controller.py
router/
summarizer/
reporter/
rag_answer/
api/
main.py
schemas.py
routes/rag_endpoint.py
utils/
log_config.py
keyvault_client.py
artifact_writer.py
data/
artifacts/<trace_id>/
logs/

yaml
Copy code

---

# 🧭 Sprint Progress Overview

| Sprint | Dates | Focus Area | Status |
|-------|--------|------------|--------|
| 1 | Oct 8 – Oct 21 | Foundations / ETL | ✅ Completed |
| 2 | Oct 22 – Nov 7 | Azure Migration | ✅ Completed |
| 3 | Nov 8 – Nov 18 | Integration Live | ✅ Completed |
| 4 | Nov 19 – Dec 2 | AI Layer (Semantic Retrieval) | ✅ Completed |
| 5 | Dec 3 – Dec 16 | RAG Finalization | ✅ Completed |
| 6 | Dec 17 – Dec 31 | **LangGraph + API Service** | **🟦 Completed (v6.0)** |

---

# 🚀 What’s New in v6.0.0 (Sprint 6)

## ✅ 1. Full LangGraph Agent Pipeline
Four agents integrated via DAG:

- **RouterAgent**  
- **SummarizerAgent**  
- **ReporterAgent**  
- **RAGAnswerAgent**

Graph flow is deterministic and validated via smoke tests.

## ✅ 2. DAGController (Production-Ready)
A single orchestrator class:

- Builds LangGraph once  
- Caches the compiled app  
- Generates **UUID trace IDs**  
- Writes artifacts  
- Returns structured responses

## ✅ 3. ArtifactWriter System
For every run:

data/artifacts/<trace_id>/
summary.txt
insights.json
retrieved_docs.json
final_answer.txt
state.json
metadata.json

makefile
Copy code

## ✅ 4. FastAPI Service (Production)
Routes:

POST /rag/query
GET /health
GET /docs

makefile
Copy code

## ✅ 5. Caddy Reverse Proxy (Azure VM)
Caddyfile:

http://4.246.99.209 {
reverse_proxy 127.0.0.1:8000
}

csharp
Copy code

Now accessible publicly.

## ✅ 6. Python Packaging (pip install -e .)
The project is now a proper Python module:

/home/seanthakur/pubmed_pipeline/pubmed_pipeline/init.py

yaml
Copy code

Imports such as `pubmed_pipeline.agents.router.router_agent` now resolve globally.

---

# 🌐 Deployment Status (Azure VM)

| Component | Status | Notes |
|----------|--------|-------|
| Azure VM | ✅ | Ubuntu / Python 3.12 |
| FastAPI (Uvicorn) | ✅ | Bound to 0.0.0.0:8000 |
| Caddy Reverse Proxy | ✅ | Serves http://4.246.99.209 |
| Swagger UI | ✅ | http://4.246.99.209/docs |
| LangGraph Pipeline | ✅ | All nodes working |
| ArtifactWriter | ✅ | Producing per-trace directories |

---

# 🧪 Validation Checklist (v6.0)

### 1. LangGraph Smoke Test
python3 -m pubmed_pipeline.agents.base.dag_controller

diff
Copy code

Expected:
- router ✔
- summarizer ✔
- reporter ✔
- rag_answer ✔
- artifacts folder created

### 2. FastAPI Local
curl http://127.0.0.1:8000/docs

python
Copy code

### 3. Public Endpoint
From any device:
http://4.246.99.209/docs

shell
Copy code

### 4. RAG Query Example
curl -X POST "http://4.246.99.209/rag/query"
-H "Content-Type: application/json"
-d '{"query":"cisplatin S-1 gastric cancer outcomes", "top_k": 3}'

yaml
Copy code

---

# 📁 Updated Directory Structure (After Packaging)

pubmed_pipeline/
pubmed_pipeline/
agents/
api/
utils/
data/
rag/
ingestion/
...
setup.py
README.md
requirements.txt
venv/

yaml
Copy code

---

# 🧠 Key Modules

### **DAGController**
- entrypoint: `pubmed_pipeline.agents.base.dag_controller`

### **ArtifactWriter**
- saves outputs/metadata per-trace

### **FastAPI Backend**
- `api/main.py`
- `api/routes/rag_endpoint.py`
- `api/schemas.py`

### **LangGraph DAG**
- defined in `dag_controller.py`

---

# 📝 Release Notes — v6.0.0

### Added
- Full agent pipeline (router → summarizer → reporter → rag_answer)
- DAGController orchestration engine
- ArtifactWriter subsystem
- FastAPI production backend
- Public Swagger UI
- Caddy reverse proxy integration
- Complete packaging as editable Python module

### Improved
- Logging
- Error handling
- Directory structure
- Import paths
- CI friendliness

### Removed
- Old smoke-test scripts
- Direct execution stubs

---

# 👤 Maintainer  
Sean Thakur (seantthakur-web)  
Environment: Azure VM (pubmed-dev-vm, West US)  
Last Updated: **Nov 13 2025**
