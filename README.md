# 🧠 PubMed + OrderPipeline Project  
**Personal Edition — Integration Live (v4)**  
by [@seantthakur-web](https://github.com/seantthakur-web)

[![GitHub Repo](https://img.shields.io/badge/repo-DBA--DE__pubmed__pipeline-blue?logo=github)](https://github.com/seantthakur-web/DBA-DE_pubmed_pipeline)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](#)
[![Status](https://img.shields.io/badge/status-Integration--Live--v4-00b894.svg)](#)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg?logo=python)](#)
[![Azure](https://img.shields.io/badge/Deployed%20on-Azure--VM-lightblue?logo=microsoftazure)](#)

---

### 🧭 Overview

This repository contains the **personal Azure-based version** of the PubMed Knowledge Graph + OrderPipeline integration project.  
Originally developed under Nestlé’s `nestle-it` organization, this edition now runs entirely under a **personal cloud environment** for continued development and experimentation.

The project demonstrates a **modern data engineering pipeline** integrating:
- Azure Blob Storage → Event Hub (Kafka mode)
- Spark Streaming → Azure OpenAI (embeddings)
- PostgreSQL + `pgvector` for semantic storage
- LangGraph / RAG integration (later sprint)
- End-to-end orchestration in Azure VM / ADF  

---

### 🧩 Current Version
**Version:** `v4 – Integration Live`  
**Focus:** Spark → EventHub → LLaMA/Azure OpenAI → pgvector  
**Status:** ✅ Embeddings verified · 🚧 Kafka Integration in progress  

---

### ⚙️ Environment Summary

| Component | Location | Purpose |
|------------|-----------|----------|
| **Compute** | Azure VM (`pubmed-dev-vm`) | Runs ETL, Spark listener, Kafka consumer |
| **Database** | Azure PostgreSQL (pgvector 0.8.0) | Vector + metadata store |
| **Storage** | Azure Blob (`raw/`, `processed/`) | PubMed ingestion & pipeline staging |
| **AI Service** | Azure OpenAI `text-embedding-ada-002` | Entity + summary embeddings |
| **Integration** | Event Hub (Kafka-compatible) | Real-time message streaming |
| **Version Control** | GitHub: [`seantthakur-web/DBA-DE_pubmed_pipeline`](https://github.com/seantthakur-web/DBA-DE_pubmed_pipeline) | Active development branch: `integration` |

---

### 🧱 Branching Model

| Branch | Base | Purpose |
|---------|------|----------|
| `main` | — | Stable base (production-ready) |
| `integration` | `main` | Sprint 3+ active development (Integration Live) |
| `feature/*` | `integration` | Sub-modules (Kafka, Spark, pgvector, etc.) |

---

### 🧠 Next Steps
- [ ] Complete Event Hub (Kafka) integration test
- [ ] Enable Spark structured streaming listener
- [ ] Store embeddings + metadata in PostgreSQL
- [ ] Prepare demo notebook for RAG flow (Sprint 5)
- [ ] Deploy ADF orchestration (Sprint 4+)

---

📫 **Maintainer:** [@seantthakur-web](https://github.com/seantthakur-web)  
🗓️ **Updated:** November 2025  

---

