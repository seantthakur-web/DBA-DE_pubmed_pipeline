# 🧬 PubMed + OrderPipeline Project  
### v4.1 – Azure Integration Live (Sprint 2 Complete)

---

## 📘 Overview

The **PubMed Knowledge Graph Pipeline** is a hands-on data engineering project designed to modernize scientific literature ingestion using Azure’s modern data stack.  
This repository mirrors the Nestlé internal stack — re-implemented in a personal Azure environment — to demonstrate full ETL, vector storage, and GenAI readiness.

---

## 🎯 Objective

Transition from Database Administrator (DBA) to Data Engineer through a 12-week sprint plan, building a real, production-style pipeline that includes:
- Data ingestion, transformation, and loading
- Stream processing with Spark + Kafka (Azure Service Bus)
- Vector embedding + AI integration (Azure OpenAI / Mistral)
- Secrets + cost management
- End-to-end deployment documentation

---

## 🗓️ Sprint Plan — Learning & Delivery Roadmap

| Sprint | Dates | Focus Area | Key Deliverables | Status |
|:--:|:--:|:--|:--|:--|
| **1️⃣** | Oct 8 – Oct 21 | 🧱 Foundations | Local ETL pipeline, GitHub repo setup, documentation standards | ✅ Completed |
| **2️⃣** | Oct 22 – Nov 7 | ☁️ Cloud Migration | Full Azure stack replication + connectivity validation | ✅ Completed |
| **3️⃣** | Nov 8 – Nov 18 | 🔁 Integration Live | Spark → Kafka → LLaMA → Vector Flow implementation | 🚧 In Progress |
| **4️⃣** | Nov 19 – Dec 2 | 🧠 AI Layer | PubMed semantic search, embeddings, and retrieval QA | ⏳ Pending |
| **5️⃣** | Dec 3 – Dec 16 | 🧩 Orchestration | Data Factory + Airflow + dbt pipeline integration | ⏳ Pending |
| **6️⃣** | Dec 17 – Dec 31 | 🚀 Final Demo | Full end-to-end showcase + recording + documentation | ⏳ Pending |

---

## 🧭 Phase 1 — Rebuild the Nestlé Stack in Personal Azure (✅ Completed Nov 7, 2025)

| Layer | Component | Status | Notes |
|:--:|:--|:--|:--|
| 1️⃣ | Resource Group | ✅ `pubmed-rg` (East US 2) | Verified via CLI |
| 2️⃣ | Azure PostgreSQL Flexible Server (+ pgvector) | ✅ `pubmed-db-test` live | pgvector v0.8 enabled + vector insert verified |
| 3️⃣ | Azure VM (for Spark + ETL) | ✅ `pubmed-dev-vm` | Python 3.12 + OpenAI SDK installed |
| 4️⃣ | Blob Storage (raw + processed) | ✅ `pubmedstorage` | Containers created + sample upload verified |
| 5️⃣ | Service Bus (Kafka-compatible) | ✅ `pubmed-ns` | End-to-end listener validated |
| 6️⃣ | Azure OpenAI / Mistral API | ✅ Integrated | `text-embedding-3-small` working |
| 7️⃣ | Key Vault (secrets) | ✅ `pubmed-kv` | Created + verified (Postgres / ServiceBus / OpenAI keys) |
| 8️⃣ | Cost Management | ✅ Verified | `az costmanagement query` confirmed usage output |

**Commit Reference:** [`2d16915`](https://github.com/seantthakur-web/DBA-DE_pubmed_pipeline/commit/2d16915fc0c25a1fdd0fa50f7cd7b3e323ed133c)  
**Timestamp:** Fri Nov 7 2025 01:01:49 UTC  (Thu Nov 6 5:01 PM PT)  
**Sprint Milestone:** `v4.1.0 – Azure Integration Live`

---

## 🏁 Sprint 2 Retrospective Summary  
**Related JIRA Tickets:** INNVO-416, INNVO-417, INNVO-418, INNVO-419  

| Focus | Outcome |
|:--|:--|
| **Pivot** | Moved from Nestlé sandbox to personal Azure subscription to bypass policy restrictions |
| **Progress** | Fully rebuilt the production Azure stack locally, validated pgvector + Service Bus integration |
| **Evidence** | Portal screenshots, CLI logs, and cost query output attached in JIRA tickets |
| **Next Focus** | Transition to Integration Live (Sprint 3): connect Spark → Kafka → Vector listeners |

---

## ⚙️ Repository Structure

DBA-DE_pubmed_pipeline/
├── configs/
├── data/
├── etl/
├── ingestion/
├── listeners/
├── logs/
├── nlp_extraction/
├── scripts/
├── spark_jobs/
├── streaming/
└── README.md

yaml
Copy code

---

## 🔐 Secrets & Security (Layer 7)

- Secrets stored in **Azure Key Vault**: `pubmed-kv`
- Added secrets:
  - `POSTGRES-CONN`
  - `SERVICEBUS-CONN`
  - `OPENAI-KEY`
- Local development uses `.env` under `.gitignore`
- Verified both CLI and Python retrieval via `DefaultAzureCredential()` (optional for Free Tier)

---

## 💰 Cost Management (Layer 8)

Executed Azure CLI query:
```bash
az rest \
  --method post \
  --uri "https://management.azure.com/subscriptions/$(az account show --query id -o tsv)/providers/Microsoft.CostManagement/query?api-version=2023-03-01" \
  --body '{"type":"Usage","timeframe":"MonthToDate","dataset":{"aggregation":{"totalCost":{"name":"PreTaxCost","function":"Sum"}}}}'
✅ Returned JSON confirms cost management is active for the Free Tier subscription.

🧠 Sprint 3 Preview — Integration Live
Listener	Description	Goal
spark_producer.py	Publish PubMed messages into Service Bus (Kafka-compatible)	Generate event stream
kafka_consumer_etl.py	Consume + transform stream messages	Stage structured payloads
llama_listener.py	Process embeddings with local LLaMA/Mistral	Create 1536-dim vectors
vector_listener.py	Insert embeddings into PostgreSQL (pgvector)	Verify retrieval + query flow

📄 License & Attribution
Maintained by Sean Thakur as part of the DBA → Data Engineer transition roadmap at Nestlé Health Science Innovation.
All configurations and scripts are for educational and demonstration use under the Nestlé Innovation Sandbox guidelines.

🏷️ Version History
Version	Date	Description
v4.1.0	Nov 7, 2025	Sprint 2 complete — Azure stack replicated successfully
v4.0.0	Oct 21, 2025	Sprint 1 complete — Local ETL setup
v3.x	Sep 2025	Pre-Azure experimental builds

Maintainer: seantthakur-web
Environment: Personal Azure (Free Tier, East US 2)
Last Updated: Nov 7, 2025
