"""
Layer 3 – ETL & Storage
Reads NLP-extracted PubMed JSON → Normalizes entities & relations → Loads into SQLite/Postgres.
"""

import os
import sys
import json
import uuid
import argparse
import glob
from datetime import datetime

# ==========================================================
# Universal path fix – ensures local imports work in any environment
# ==========================================================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)
# ==========================================================

from db_utils import connect_db, insert_entities, insert_relations, insert_paper
from schema_definitions import create_tables


# ----------------------------------------------------------
# 🧩 Normalization utilities
# ----------------------------------------------------------
def normalize_entity(e):
    """Clean text and assign a unique ID."""
    return {
        "entity_id": uuid.uuid4().hex,
        "name": e["text"].strip().lower(),
        "type": e["label"]
    }


def normalize_relation(r, entity_lookup):
    """Convert relation into ID-based format."""
    subj = r.get("subject", "").strip().lower()
    obj = r.get("object", "").strip().lower()
    return {
        "relation_id": uuid.uuid4().hex,
        "subject_id": entity_lookup.get(subj),
        "predicate": r.get("predicate", ""),
        "object_id": entity_lookup.get(obj)
    }


# ----------------------------------------------------------
# 🧠 ETL Core Logic
# ----------------------------------------------------------
def process_file(input_path, conn):
    """ETL for one or many NLP-extracted JSON records."""
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"🔍 Processing PubMed file: {input_path}")

    records = data if isinstance(data, list) else [data]
    total_entities, total_relations = 0, 0

    for record in records:
        entities = [normalize_entity(e) for e in record.get("entities", [])]
        entity_lookup = {e["name"]: e["entity_id"] for e in entities}

        relations = []
        for r in record.get("relations", []):
            rel = normalize_relation(r, entity_lookup)
            if rel["subject_id"] and rel["object_id"]:
                relations.append(rel)

        paper = {
            "pmid": record.get("pmid"),
            "title": record.get("title"),
            "abstract": record.get("abstract")
        }

        insert_paper(conn, paper)
        insert_entities(conn, entities)
        insert_relations(conn, relations)

        total_entities += len(entities)
        total_relations += len(relations)

    print(f"💾 Saved {total_entities} entities, {total_relations} relations → DB\n")


# ----------------------------------------------------------
# 🚀 CLI entry point
# ----------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="ETL – Normalize and store PubMed extraction data."
    )
    parser.add_argument("--input", required=True, help="Path or wildcard to NLP-extracted JSON file(s)")
    parser.add_argument("--db", default="data/storage/pubmed_etl.db", help="Path to SQLite DB")
    args = parser.parse_args()

    # 🔧 Expand wildcard patterns (Windows-safe)
    if "*" in args.input or "?" in args.input:
        matches = glob.glob(args.input)
        if not matches:
            raise FileNotFoundError(f"No files match pattern: {args.input}")
        matches.sort(key=os.path.getmtime)
        args.input = matches[-1]
        print(f"📄 Auto-selected latest file: {os.path.basename(args.input)}")

    os.makedirs(os.path.dirname(args.db), exist_ok=True)
    conn = connect_db(args.db)
    create_tables(conn)

    process_file(args.input, conn)

    conn.commit()
    conn.close()
    print("✅ ETL completed successfully.")


if __name__ == "__main__":
    main()
