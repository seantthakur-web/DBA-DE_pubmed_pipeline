import os
import json
import glob
import psycopg2
from textwrap import wrap
from openai import AzureOpenAI

# -----------------------------
# Environment Variables
# -----------------------------
DB_HOST = os.getenv("PGHOST")
DB_NAME = os.getenv("PGDATABASE")
DB_USER = os.getenv("PGUSER")
DB_PASS = os.getenv("PGPASSWORD")

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# -----------------------------
# Azure OpenAI client
# -----------------------------
client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version="2024-06-01",
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

# -----------------------------
# PostgreSQL connection
# -----------------------------
def get_pg_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        sslmode="require"
    )

# -----------------------------
# Extract abstract text
# -----------------------------
def extract_abstract(pubmed_json):
    try:
        article = pubmed_json["MedlineCitation"]["Article"]
        abstract_obj = article.get("Abstract", {})
        paragraphs = abstract_obj.get("AbstractText", [])
        return "\n".join(paragraphs)
    except Exception:
        return ""

# -----------------------------
# Chunk text
# -----------------------------
def chunk_text(text, chunk_size=500):
    return wrap(text, chunk_size)

# -----------------------------
# Create embedding
# -----------------------------
def embed_text(text):
    response = client.embeddings.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        input=text
    )
    return response.data[0].embedding

# -----------------------------
# Insert into PGVector table
# -----------------------------
def insert_chunk(cur, pmid, chunk_id, content, embedding):
    cur.execute("""
        INSERT INTO pubmed_embeddings (pmid, chunk_id, content, embedding)
        VALUES (%s, %s, %s, %s)
    """, (pmid, chunk_id, content, embedding))

# -----------------------------
# Main ingestion from raw_pubmed directory
# -----------------------------
def ingest_raw_pubmed():
    conn = get_pg_connection()
    cur = conn.cursor()

    raw_path = "pubmed_pipeline/data/raw_pubmed/*.json"
    files = glob.glob(raw_path)

    total_chunks = 0

    for file_path in files:
        with open(file_path, "r") as f:
            pubmed_json = json.load(f)

        pmid = pubmed_json["MedlineCitation"]["PMID"]
        abstract = extract_abstract(pubmed_json)

        if not abstract:
            continue  # Skip papers with no abstract

        chunks = chunk_text(abstract)

        for idx, chunk in enumerate(chunks):
            embedding = embed_text(chunk)
            insert_chunk(cur, pmid, idx, chunk, embedding)
            total_chunks += 1

        conn.commit()
        print(f"Inserted {len(chunks)} chunks for PMID {pmid}")

    cur.close()
    conn.close()
    print(f"Ingestion complete. Total chunks inserted: {total_chunks}")


if __name__ == "__main__":
    ingest_raw_pubmed()
