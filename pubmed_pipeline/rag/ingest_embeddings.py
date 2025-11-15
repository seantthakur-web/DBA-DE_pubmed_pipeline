import os
import json
import psycopg2
import tiktoken
from datetime import datetime
from textwrap import wrap
from openai import AzureOpenAI

# -----------------------------
# Load environment variables
# -----------------------------
DB_HOST = os.getenv("PGHOST")
DB_NAME = os.getenv("PGDATABASE")
DB_USER = os.getenv("PGUSER")
DB_PASS = os.getenv("PGPASSWORD")

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # e.g. "gpt-4o-mini-embed"

# -----------------------------
# Initialize Azure OpenAI
# -----------------------------
client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version="2024-06-01",
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

# -----------------------------
# Simple chunking function
# -----------------------------
def chunk_text(text, chunk_size=500):
    """Split text into fixed-size chunks."""
    return wrap(text, chunk_size)

# -----------------------------
# Make embeddings
# -----------------------------
def embed_text(text: str):
    response = client.embeddings.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        input=text
    )
    return response.data[0].embedding

# -----------------------------
# Connect to PostgreSQL
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
# Insert into PGVector table
# -----------------------------
def insert_embedding(cur, pmid, chunk_id, content, embedding):
    cur.execute(
        """
        INSERT INTO pubmed_embeddings (pmid, chunk_id, content, embedding)
        VALUES (%s, %s, %s, %s)
        """,
        (pmid, chunk_id, content, embedding)
    )

# -----------------------------
# Main ingestion loop
# -----------------------------
def ingest_pubmed_file(json_path):
    conn = get_pg_connection()
    cur = conn.cursor()

    with open(json_path, "r") as f:
        papers = json.load(f)

    total_chunks = 0

    for paper in papers:
        pmid = paper.get("pmid")
        abstract = paper.get("abstract", "")

        chunks = chunk_text(abstract, chunk_size=500)

        for idx, chunk in enumerate(chunks):
            embedding = embed_text(chunk)
            insert_embedding(cur, pmid, idx, chunk, embedding)
            total_chunks += 1

        conn.commit()

    cur.close()
    conn.close()

    print(f"Ingestion complete. Total chunks inserted: {total_chunks}")


if __name__ == "__main__":
    # Example file path — update if needed
    json_path = "/home/seanthakur/pubmed_pipeline/pubmed_pipeline/data/extracted/nlp_extracted_20251006_0918.json"

    print("Starting embedding ingestion...")
    ingest_pubmed_file(json_path)
