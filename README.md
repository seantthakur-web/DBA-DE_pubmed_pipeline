PubMed AI System
v6.0.0 – Agentic LangGraph RAG + FastAPI (Azure Production Build)

This release upgrades the PubMed Pipeline from a local prototype into a production-grade biomedical question-answering service running entirely on Azure infrastructure.

It includes:

LangGraph multi-agent reasoning pipeline

FastAPI backend (public HTTP endpoint via Caddy)

pgvector-based semantic retrieval

Azure OpenAI (embeddings + LLM completions)

Artifact logging for trace-level reproducibility

Modular Python package (pip install -e .)

Updated PubMed ingestion pipeline (≈900 chunks)

The system now supports end-to-end biomedical RAG, deployed on an Azure VM as a service.

1. Overview

The PubMed RAG pipeline ingests biomedical abstracts, embeds them using Azure OpenAI, stores them in PostgreSQL pgvector, and exposes a LangGraph-powered multi-agent workflow via FastAPI.

The full stack includes:

Azure VM (Ubuntu 22.04)

FastAPI + Uvicorn

Caddy reverse proxy (public access)

PostgreSQL Flexible Server + pgvector

Azure OpenAI (embeddings + LLM)

LangGraph multi-agent DAG

ArtifactWriter for traceable outputs

2. High-Level Architecture (v6.0)
User Query
   ↓
FastAPI (/rag/query)
   ↓
DAGController (trace_id created)
   ↓
LangGraph DAG Execution
   ├── Router Agent
   ├── Summarizer Agent
   ├── Reporter Agent
   └── RAG Answer Agent
   ↓
ArtifactWriter → data/artifacts/<trace_id>/
   ↓
JSON Response returned to client/UI

3. LangGraph DAG (v6.0)

The system uses a 4-node deterministic pipeline:

Node	Description
router	Generates embeddings → runs pgvector similarity search → prepares retrieved_docs
summarizer	Produces multi-bullet summaries of retrieved evidence
reporter	Extracts structured clinical/biomedical insights
rag_answer	Produces final grounded answer with optional PMIDs

Execution order is captured in execution_order.

4. FastAPI Backend
Endpoints
Method	Route	Purpose
POST	/rag/query	Main agentic RAG endpoint
GET	/health	Health check
GET	/docs	Swagger UI

FastAPI uses the DAGController internally to execute LangGraph, create trace IDs, and generate artifacts.

5. Artifact System

For every user query, the system generates:

pubmed_pipeline/data/artifacts/<trace_id>/
│
├── final_answer.txt
├── summary.txt
├── insights.json
├── retrieved_docs.json
├── state.json
└── metadata.json


Uses:

Auditing

Debugging

Explainability

Reproducibility

This supports research-grade observability.

6. Deployment Status (Azure)
Component	Status	Notes
Azure VM	✔	Python 3.12, Uvicorn running on port 8000
Caddy	✔	Public reverse proxy → exposes /docs
FastAPI	✔	Available externally
LangGraph Agents	✔	All nodes integrated
ArtifactWriter	✔	Producing full trace runs
pgvector Ingestion	✔	~900 chunks (225 abstracts)

Public Swagger UI:

http://4.246.99.209/docs

7. Directory Structure (After Packaging)
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
│   ├── utils/
│   │   ├── log_config.py
│   │   ├── artifact_writer.py
│   │   ├── keyvault_client.py
│   │
│   ├── data/
│   │   ├── artifacts/
│   │   └── storage/
│   │
│   ├── etl/
│   │   ├── rebuild_papers_from_pubmed_query.py
│   │
│   └── __init__.py
│
├── requirements.txt
├── setup.py
└── README.md

8. Sprint Progress
Sprint	Dates	Objective	Status
1	Oct 8 – Oct 21	ETL Foundations	✔ Completed
2	Oct 22 – Nov 7	Azure Migration	✔ Completed
3	Nov 8 – Nov 18	Integration Live	✔ Completed
4	Nov 19 – Dec 2	Semantic Retrieval	✔ Completed
5	Dec 3 – Dec 16	RAG Finalization	✔ Completed
6	Dec 17 – Dec 31	LangGraph + API Service	✔ Completed
9. Validation Checklist (v6.0)
Smoke Test
python3 -m pubmed_pipeline.agents.base.dag_controller


Expected results:

Router ✔

Summarizer ✔

Reporter ✔

Rag Answer ✔

Artifacts generated ✔

FastAPI Health
curl http://127.0.0.1:8000/health

Public Endpoint
http://4.246.99.209/docs

Sample Query
curl -X POST "http://4.246.99.209/rag/query" \
  -H "Content-Type: application/json" \
  -d '{"query":"cisplatin S-1 gastric cancer outcomes", "top_k": 3}'

10. Maintainer

Sean Thakur
Azure VM: pubmed-dev-vm (West US)
GitHub: https://github.com/seantthakur-web/DBA-DE_pubmed_pipeline

Last Updated: Nov 15, 2025
