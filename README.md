# 🧠 PubMed Knowledge Graph Pipeline

This repository demonstrates an end-to-end AI Data Engineering pipeline that ingests PubMed research papers, applies NLP entity extraction, performs ETL transformations, and prepares the data for graph loading (Neo4j) and analytics.

---

## 🚀 Project Overview

| Layer | Component | Description |
|-------|------------|-------------|
| **1️⃣ Ingestion** | `ingestion/pubmed_fetch.py` | Queries PubMed (e.g., “gastric cancer AND nutrition”), saves abstracts locally. |
| **2️⃣ Streaming (Kafka Stub)** | `streaming/kafka_producer_stub.py` | Simulates real-time PubMed messages written to `/data/streaming/`. |
| **3️⃣ NLP Extraction** | `nlp_extraction/nlp_extractor.py` | Uses BioBERT (`d4data/biomedical-ner-all`) to extract biomedical entities. |
| **4️⃣ ETL Transformation** | `etl/etl_transform.py` | Cleans, structures, and stores extracted data into normalized tables. |
| **5️⃣ Storage / Graph Prep** | `data/storage/pubmed_etl.db` | SQLite DB ready for Neo4j loading and downstream analytics. |

---

## 📂 Directory Structure

data/
┣ raw_pubmed/ # Raw PubMed XML/JSON downloads
┣ streaming/ # Simulated Kafka JSONs
┣ extracted/ # BioBERT entity extraction output
┗ storage/ # Final ETL output (SQLite DB)
etl/
┣ etl_transform.py
┣ verify_etl.py
streaming/
┗ kafka_producer_stub.py
ingestion/
┗ pubmed_fetch.py
nlp_extraction/
┗ nlp_extractor.py



---

## 🧩 ETL Processing (Transformation Layer)

This layer structures extracted PubMed abstracts into relational tables ready for Neo4j ingestion.

### 📂 Input
`/data/extracted/nlp_extracted_*.json` — entity-annotated data from the BioBERT extraction layer.

### 📤 Output
`/data/storage/pubmed_etl.db` — SQLite database containing normalized tables:

| Table | Description | Example Count |
|--------|--------------|----------------|
| `papers` | PubMed abstracts with titles, abstracts, and PMIDs | 20 |
| `entities` | Extracted biomedical entities (name, type, entity_id) | 646 |
| `relations` | Placeholder for future relation extraction | 0 |

### 🧱 Schema Overview

**papers**

| Column | Type | Description |
|---------|------|-------------|
| pmid | String | PubMed Identifier |
| title | String | Cleaned article title |
| abstract | String | Cleaned abstract text |

**entities**

| Column | Type | Description |
|---------|------|-------------|
| entity_id | String | Unique identifier (UUID) |
| name | String | Extracted entity token |
| type | String | Entity category (e.g., Medication, Symptom, Therapeutic_procedure) |

**relations**

| Column | Type | Description |
|---------|------|-------------|
| subject_id | String | Entity acting as subject |
| object_id | String | Entity acting as object |
| relation_type | String | Relation label (to be populated later) |

---

### ⚙️ Run Instructions

```bash
# Activate virtual environment
.\.venv\Scripts\activate

# Execute full pipeline
.\run_pipeline.ps1

After successful execution:
✅ All layers completed successfully!
📊 Check your results in: data/storage/pubmed_etl.db

🧾 Verification Example

import sqlite3, pandas as pd
conn = sqlite3.connect("data/storage/pubmed_etl.db")

print(pd.read_sql_query("SELECT * FROM papers LIMIT 3;", conn))
print(pd.read_sql_query("SELECT * FROM entities LIMIT 3;", conn))
print(pd.read_sql_query("SELECT COUNT(*) FROM relations;", conn))

conn.close()


🧠 Notes

Week 7 output format: SQLite (.db) for validation and debugging.

Week 8 will evolve to Parquet using PySpark for dbt/Airflow optimization.

The relations table is reserved for future expansion of entity relationships in Neo4j.

✅ Current Status
Sprint	Focus	Status
        Python   ETL + Environment Setup	✅ Done (This was done prior to added to innovation sprints)
Sprint 1	PySpark Transformation + Entity Extraction	✅ Done
Sprint 2	 Airflow / dbt Integration	🚧 Upcoming (starts in october 22nd)


## 🧩 Next Steps

1. **Transition ETL Output to Parquet Format (Week 8)**  
   Convert current SQLite output (`pubmed_etl.db`) to columnar **Parquet** format using PySpark to support dbt modeling and downstream analytics.

2. **Create Airflow DAG for Full Orchestration**  
   Build an Airflow workflow that automates the PubMed pipeline from ingestion → NLP → ETL → storage, ensuring end-to-end scheduling and monitoring.

3. **Develop Neo4j Loader for Graph Population**  
   Design Cypher scripts and a loader module to transform the structured data (papers → entities → relations) into a Neo4j graph database.

4. **Integrate LangGraph / RAG Pipeline for AI Retrieval**  
   Extend the system with **LangGraph** to enable retrieval-augmented generation (RAG) over biomedical graph data, improving context-aware question answering.

Author: Sean T.
Maintainer: Data Engineering Track (DBA → DE Transition) with AI layers :)




