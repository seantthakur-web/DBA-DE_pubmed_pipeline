# 🧬 PubMed + OrderPipeline Project  
### v5.0 – RAG Pipeline Finalization (Azure Integration Live)

---

## 📘 Overview  
The **PubMed Knowledge Graph Pipeline** has matured from a local ETL demo into a fully cloud-integrated **Retrieval-Augmented Generation (RAG)** system.  
It now runs end-to-end across **Azure OpenAI**, **PostgreSQL (pgvector)**, **Azure Key Vault**, and **FastAPI**, enabling semantic retrieval and LLM-based generation over biomedical abstracts.

This phase completes the transition from foundational ETL (Sprints 1–3) to a production-style AI pipeline.

---

## 🎯 Objective  
Continue the 12-week DBA → Data Engineer transition plan by extending the integration layer to support a live RAG workflow:

- Secure secrets via **Azure Key Vault**
- Retrieve embeddings from **PostgreSQL pgvector**
- Generate contextual answers using **GPT-4o**
- Expose the full flow through **FastAPI**
- Add centralized, rotating logging for observability

---

## 🧭 Phase 3 — Integration Live (✅ Completed Nov 9 2025)

| Layer | Component | Status | Notes |
|:--|:--|:--|:--|
| 1️⃣ | Resource Group | ✅ pubmed-rg (West US) | Verified via CLI |
| 2️⃣ | PostgreSQL Flexible Server (+ pgvector) | ✅ pubmed-db-test | `pgvector` v0.8 enabled, vector insert validated |
| 3️⃣ | Azure VM (for Spark + ETL) | ✅ pubmed-dev-vm | Python 3.12 + SDKs installed |
| 4️⃣ | Blob Storage (raw + processed) | ✅ pubmedstorage | Containers verified |
| 5️⃣ | Service Bus (Kafka) | ✅ pubmed-ns | Topic + subscription validated |
| 6️⃣ | Azure OpenAI (Embeddings) | ✅ text-embedding-3-small | Embedding API verified |
| 7️⃣ | Key Vault | ✅ pubmed-kv | Postgres / ServiceBus / OpenAI keys secured |
| 8️⃣ | Cost Management | ✅ Active | CLI usage query validated |

Commit Ref: `v4.2.0`  |  Timestamp: Nov 9 2025  |  Milestone: **Integration Live Complete**

---

## 🧠 Phase 4 — AI Layer (Sprint 4 ✅ Completed)

This sprint introduced the **semantic retrieval foundation** that made the RAG pipeline possible.  
It focused on building the retriever logic, vector search prototypes, and integrating the first mock LLM responses before live Azure OpenAI access.

| Layer | Component | Status | Notes |
|:--|:--|:--|:--|
| 1️⃣ | pgvector Integration | ✅ | Similarity search validated with sample vectors |
| 2️⃣ | Retriever Prototype | ✅ | Early version of `rag_retriever.py` completed |
| 3️⃣ | Generator Stub | ✅ | LLM stub responses integrated with retriever |
| 4️⃣ | Local API Demo | ✅ | `/rag/query` scaffold tested locally |
| 5️⃣ | Observability | ✅ | Logging refactored for multi-module support |

Commit Ref: `v4.5.0`  |  Timestamp: Nov 25 2025  |  Milestone: **AI Layer (Semantic Retrieval QA)**

---

## 🧭 Phase 5 — RAG Pipeline Finalization (✅ Completed Nov 12 2025)

| Layer | Component | Status | Notes |
|:--|:--|:--|:--|
| 1️⃣ | Azure Key Vault | ✅ Integrated | Secrets retrieved via `utils/keyvault_client.py` |
| 2️⃣ | Logging | ✅ Unified | `utils/log_config.py` writes to `/data/logs/rag_pipeline/rag.log` |
| 3️⃣ | Retriever Module | ✅ Ready | pgvector similarity search validated |
| 4️⃣ | Generator Module | ✅ Live | `gpt-4o` Azure OpenAI deployment connected |
| 5️⃣ | FastAPI Endpoint | ✅ Running | `/rag/query` tested with local Uvicorn |
| 6️⃣ | Documentation | ✅ This README v5.0 | Updated setup & validation instructions |

Commit Ref: `v5.0.0`  |  Timestamp: Nov 12 2025  |  Milestone: **Azure RAG Integration Live**

---

## ⚙️ Azure Setup

### 🔐 Key Vault Secrets
```bash
az keyvault secret set --vault-name pubmed-kv --name "azure-openai-endpoint" --value "https://pubmed-ai-westus.openai.azure.com"
az keyvault secret set --vault-name pubmed-kv --name "azure-openai-key" --value "<your-openai-key>"
export AZURE_OPENAI_DEPLOYMENT="gpt-4o"
🧠 Azure OpenAI Deployments
Role	Model	Deployment Name	Status
Embeddings	text-embedding-ada-002	text-embedding-ada-002	✅ Active
Chat / Generation	gpt-4o	gpt-4o	✅ Active

🧩 Local Structure
bash
Copy code
pubmed_pipeline/
├── utils/                 → Key Vault & Logger
├── rag/                   → Retriever, Generator, API
├── data/logs/rag_pipeline → Unified log output
├── etl/                   → PostgreSQL + Spark ingestion
└── docs/demos/            → Demo scripts & notes
🧪 Module Tests
1️⃣ Key Vault Connection
bash
Copy code
python3 -m pubmed_pipeline.utils.keyvault_client
✅ Expected: log entry under data/logs/rag_pipeline/rag.log

2️⃣ Generator Test
bash
Copy code
python3 -m pubmed_pipeline.rag.rag_generator
Sample Output

json
Copy code
{
  "query": "cisplatin S-1 gastric cancer outcomes",
  "answer": "The combination of cisplatin and S-1 in gastric cancer has been shown to improve clinical outcomes.",
  "context_used": 2
}
3️⃣ FastAPI Endpoint
bash
Copy code
python3 -m pubmed_pipeline.rag.api_demo
curl "http://127.0.0.1:8000/rag/query?query=cisplatin%20S-1%20gastric%20cancer%20outcomes&top_k=3"
🪵 Centralized Logging (INNVO-490)
Unified log file:
~/pubmed_pipeline/data/logs/rag_pipeline/rag.log

Example

yaml
Copy code
2025-11-12 18:27:48 | INFO | utils.log_config | Logger test confirmed.
2025-11-12 18:31:23 | INFO | rag.rag_generator | ✅ Response from Azure OpenAI.
2025-11-12 18:34:13 | INFO | rag.api_demo | ✅ RAG pipeline completed in 3101 ms.
📊 Sprint Summary
Ticket	Module	Description	Status
INNVO-489	Key Vault Integration	Secrets from pubmed-kv	✅
INNVO-490	Centralized Logging	Rotation-based logger	✅
INNVO-491	FastAPI Endpoint	/rag/query	✅
INNVO-492	RAG Generator	GPT-4o generation	✅
INNVO-493	RAG Retriever	pgvector search	✅
INNVO-494	Documentation Update	README v5.0	🟡 In Progress

🏁 Validation Checklist
Step	Test	Result
Key Vault retrieval	python3 -m pubmed_pipeline.utils.keyvault_client	✅
RAG generation	python3 -m pubmed_pipeline.rag.rag_generator	✅
FastAPI query	/rag/query	✅
Unified logging	rag_pipeline/rag.log	✅

🗓️ Sprint Plan — Learning & Delivery Roadmap
Sprint	Dates	Focus Area	Key Deliverables	Status
1️⃣	Oct 8 – Oct 21	🧱 Foundations	Local ETL setup	✅
2️⃣	Oct 22 – Nov 7	☁️ Cloud Migration	Azure stack replication	✅
3️⃣	Nov 8 – Nov 18	🔁 Integration Live	Spark → Kafka → pgvector	✅
4️⃣	Nov 19 – Dec 2	🧠 AI Layer	Semantic retrieval + QA	✅
5️⃣	Dec 3 – Dec 16	🧩 RAG Finalization	Azure OpenAI + FastAPI	✅ (v5.0)
6️⃣	Dec 17 – Dec 31	🚀 Final Demo	Docs + benchmarks	⏳

🧾 Version History
Version	Date	Description
v5.0.0	Nov 12 2025	Sprint 5 Complete — RAG Pipeline Live
v4.5.0	Nov 25 2025	Sprint 4 Complete — AI Layer (Semantic Retrieval QA)
v4.2.0	Nov 9 2025	Sprint 3 Complete — Integration Live
v4.1.0	Nov 7 2025	Azure Stack Replication
v4.0.0	Oct 21 2025	Local ETL Setup

Maintainer: Sean Thakur (seantthakur-web)
Environment: Azure VM (pubmed-dev-vm, West US)
Last Updated: Nov 12 2025


