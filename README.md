# 🧭 PubMed + OrderPipeline Project  
**Version v4.1 – Azure Integration Live**

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/seantthakur-web/DBA-DE_pubmed_pipeline?label=latest%20release)](https://github.com/seantthakur-web/DBA-DE_pubmed_pipeline/releases)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/seantthakur-web/DBA-DE_pubmed_pipeline?label=open%20PRs)](https://github.com/seantthakur-web/DBA-DE_pubmed_pipeline/pulls)
[![GitHub commits](https://img.shields.io/github/last-commit/seantthakur-web/DBA-DE_pubmed_pipeline/main?label=last%20commit)](https://github.com/seantthakur-web/DBA-DE_pubmed_pipeline/commits/main)

---

## 🧩 Overview
This repository hosts the **PubMed + OrderPipeline Knowledge Graph Pipeline**, an end-to-end data-engineering system built as part of the *DBA → Data Engineer Learning Track*.

The **v4.1 – Azure Integration** release merges all Azure cloud components—VM listener, OpenAI embeddings, pgvector storage, and ADF orchestration—into the unified main branch.

---

## 🚀 Highlights (v4.1 – Azure Integration)
- Added **Azure Data Factory orchestration** and pipeline scripts  
- Configured **PostgreSQL + pgvector** connection utilities  
- Integrated **Spark listener + Azure OpenAI embedding workflow**  
- Added safe `.env.example` template and cleaned `.gitignore`  
- Verified end-to-end flow on **personal Azure VM (pubmed-dev-vm)**  
- Tagged and released as **v4.1-AzureIntegration**

---

## 📁 Directory Structure
DBA-DE_pubmed_pipeline/
├── configs/ # Configuration files (YAML / JSON)
├── data/ # Local datasets (excluded from Git)
├── etl/ # Core ETL scripts
├── ingestion/ # Ingestion pipelines for PubMed abstracts
├── listeners/ # Azure + Spark listeners (LLaMA, Kafka)
│ └── llama_listener.py
├── utils/ # Utility modules (e.g., db_connection.py)
├── logs/ # Runtime logs for listener & pipeline runs
├── .env.example # Safe environment template
└── README.md # Project documentation

yaml
Copy code

---

## 📆 Release Timeline
| Version | Milestone | Date | Notes |
|----------|------------|------|-------|
| **v4.1** | Azure Integration Live | Nov 2025 | ADF, OpenAI embeddings, pgvector pipeline |
| **v4.0** | Integration Local | Oct 2025 | Spark → Kafka → OpenAI local flow |
| **v3.0** | Cloud Migration | Sep 2025 | PostgreSQL + Blob Storage setup |
| **v2.0** | Foundations | Aug 2025 | ETL pipeline and local environment |
| **v1.0** | Initial Commit | Jul 2025 | Repo bootstrap and README |

---

## 🧭 Next Milestone (v5.0 – ADF Automation)
**Goal:** Automate orchestration of the Spark → Kafka → OpenAI flow using Azure Data Factory pipelines.  
- Add ADF-triggered notebook execution  
- Automate vector updates to PostgreSQL  
- Integrate event-driven runs with Event Hub  
- Extend monitoring via Azure Log Analytics  

---

## 🧠 Maintainer
**Sean Thakur (@seantthakur-web)**  
Personal Azure Edition – Integration Live (v4.1)  
📍 West US Region | ☁️ Azure VM (`pubmed-dev-vm`) | 🧩 PostgreSQL 17 + pgvector 0.8.0
