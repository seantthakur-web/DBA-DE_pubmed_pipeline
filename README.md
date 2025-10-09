# 🧠 DBA-DE PubMed Pipeline

**AI-driven Data Engineering pipeline built during the DBA ➜ Data Engineer transition.**

This project demonstrates an end-to-end data pipeline that ingests PubMed research papers, streams them through Kafka, processes them with PySpark, and prepares them for loading into a Neo4j knowledge graph.  
The system simulates how **streaming biomedical data** can be transformed into **graph-based insights** for future **RAG (Retrieval-Augmented Generation)** applications.

---

## 🚀 Project Overview

| Layer | Component | Description |
|-------|------------|-------------|
| **1️⃣ Ingestion** | `ingestion/pull_pubmed.py` | Queries PubMed (e.g., “gastric cancer AND nutrition”), saves abstracts locally. |
| **2️⃣ Streaming (Kafka)** | `streaming/kafka_producer_stub.py` | Simulates real-time streaming of PubMed abstracts as Kafka messages. |
| **3️⃣ ETL (PySpark)** | `streaming/pyspark/transformers/` | Cleans and transforms text before graph loading. |
| **4️⃣ Graph Loader (Neo4j)** | `graph/neo4j_loader.py` *(planned)* | Loads 646 biomedical entities and 20 papers into Neo4j for visualization. |
| **5️⃣ RAG Layer** | *(planned)* | Enables LLM-powered querying on top of the knowledge graph. |

---

## 🧩 Architecture Diagram (Conceptual)

