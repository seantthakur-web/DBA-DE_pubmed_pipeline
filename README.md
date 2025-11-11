# 🧬 PubMed + OrderPipeline Project  
### v4.2 – Integration Live Complete (Sprint 3)

---

## 📘 Overview  
The **PubMed Knowledge Graph Pipeline** is a hands-on data-engineering project that modernizes scientific-literature ingestion using Azure’s modern data stack.  
This repository mirrors the Nestlé internal stack — re-implemented in a personal Azure environment — to demonstrate full ETL, streaming, vector storage, and GenAI readiness.

---

## 🎯 Objective  
Transition from **Database Administrator (DBA)** to **Data Engineer** through a 12-week sprint plan, building a production-style pipeline that includes:

- Ingestion → Transformation → Loading  
- Stream processing with **Spark + Azure Service Bus (Kafka-mode)**  
- Vector embedding with **Azure OpenAI**  
- Secure secret management and cost tracking  
- Full end-to-end deployment documentation  

---

## 🗓️ Sprint Plan — Learning & Delivery Roadmap

| Sprint | Dates | Focus Area | Key Deliverables | Status |
|:--:|:--|:--|:--|:--|
| 1️⃣ | Oct 8 – Oct 21 | 🧱 Foundations | Local ETL pipeline, repo setup, documentation | ✅ Completed |
| 2️⃣ | Oct 22 – Nov 7 | ☁️ Cloud Migration | Azure stack replication + connectivity | ✅ Completed |
| 3️⃣ | Nov 8 – Nov 18 | 🔁 Integration Live | Spark → Service Bus → Azure AI → pgvector flow validated | ✅ Completed (v4.2.0) |
| 4️⃣ | Nov 19 – Dec 2 | 🧠 AI Layer | PubMed semantic search + retrieval QA | ⏳ Pending |
| 5️⃣ | Dec 3 – Dec 16 | 🧩 Orchestration | ADF + Airflow + dbt pipeline | ⏳ Pending |
| 6️⃣ | Dec 17 – Dec 31 | 🚀 Final Demo | Full showcase + recording + docs | ⏳ Pending |

---

## 🧭 Phase 1 — Rebuild the Nestlé Stack (✅ Completed Nov 7 2025)

| Layer | Component | Status | Notes |
|:--|:--|:--|:--|
| 1️⃣ | Resource Group | ✅ pubmed-rg (East US 2) | Verified via CLI |
| 2️⃣ | PostgreSQL Flexible Server (+ pgvector) | ✅ pubmed-db-test live | pgvector v0.8 enabled + vector insert verified |
| 3️⃣ | Azure VM (for Spark + ETL) | ✅ pubmed-dev-vm | Python 3.12 + SDKs installed |
| 4️⃣ | Blob Storage (raw + processed) | ✅ pubmedstorage | Containers verified |
| 5️⃣ | Service Bus (Kafka) | ✅ pubmed-ns | Topic + subscription validated |
| 6️⃣ | Azure OpenAI | ✅ Integrated | `text-embedding-3-small` verified |
| 7️⃣ | Key Vault | ✅ pubmed-kv | Postgres / ServiceBus / OpenAI keys secured |
| 8️⃣ | Cost Management | ✅ Active | CLI usage query validated |

Commit Ref: `v4.1.0`  |  Timestamp: Nov 7 2025  |  Milestone: **Azure Integration Live**

---

## ⚙️ Phase 2 — Integration Live (Sprint 3 ✅ Complete)

| Phase | Description | Key Deliverables | Status |
|:--|:--|:--|:--|
| 3.1 – VM & Env Setup | Activate VM, create venv, install SDKs | Pip list verified | ✅ Complete |
| 3.2 – Service Bus Topic + Subscription | Create and test `pubmed-ns/pubmed-topic/pubmed-sub` | Message routing confirmed | ✅ Complete |
| 3.3 – Producer ↔ Consumer Flow | `spark_producer.py` ↔ `kafka_consumer_etl.py` | “Hello from Spark → Service Bus 🚀” validated | ✅ Complete |
| 3.4 – Embedding & pgvector Integration | `pubmed_ai_vector_listener.py` consumes JSON, calls Azure AI, upserts to Postgres | ✅ Stored PMID 2055453 embedding | ✅ Complete |
| 3.5 – Validation (E2E) | Verified end-to-end flow + DB persistence | `SELECT pmid, title, created_at` returns record | ✅ Complete |

---

### 🧠 Key Evidence
- Service Bus topic message confirmed:  
  `✅ Message sent to Service Bus topic: pubmed-topic`  
- Consumer log output:  
  ```json
  {
    "source": "spark_producer",
    "timestamp": 1762531926.185,
    "content": "Hello from Spark → Service Bus 🚀"
  }
Azure AI embedding log:
🧠 Embedding PMID 2055453: Phase III FLAGS Trial – Cisplatin and S-1 vs Cisplatin and 5-FU
✅ Stored / updated embedding for PMID 2055453

🧾 Sprint 3 Retrospective Summary
JIRA Tickets: INNVO-472 to INNVO-474

Focus	Outcome
Infrastructure	VM + SDK setup validated
Messaging Flow	Producer → Consumer loop validated
AI Integration	Azure OpenAI embeddings stored in Postgres (pgvector)
Verification	SQL query confirmed data persistence
Release	v3.0.0 tag pushed to GitHub (End-to-End Integration Live)

🧩 Next Focus — Sprint 4 (Orchestration)
Implement workflow control with Azure Data Factory, dbt, and Airflow for automated runs of the entire pipeline.

⚙️ Repository Structure
bash
Copy code
DBA-DE_pubmed_pipeline/
├── configs/
│   └── .env
├── listeners/
│   ├── spark_producer.py
│   ├── kafka_consumer_etl.py
│   └── pubmed_ai_vector_listener.py
├── logs/
├── .venv/
└── README.md
🧠 Secrets & Security
Secrets stored in Azure Key Vault (pubmed-kv)

.env for local testing under .gitignore

Verified access for Postgres, Service Bus, and OpenAI API keys

🏷️ Version History
Version	Date	Description
v4.2.0	Nov 9 2025	Sprint 3 Complete — Integration Live (End-to-End Validated)
v4.1.0	Nov 7 2025	Sprint 2 Complete — Azure Stack Replication
v4.0.0	Oct 21 2025	Sprint 1 Complete — Local ETL Setup

Maintainer: Sean Thakur (seantthakur-web)
Environment: Personal Azure (Free Tier – East US 2)
Last Updated: Nov 9 2025


