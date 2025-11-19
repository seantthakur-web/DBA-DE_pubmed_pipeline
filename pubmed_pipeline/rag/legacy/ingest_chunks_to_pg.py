import os
import sqlite3
import psycopg2
from typing import List, Tuple
from textwrap import wrap
from pubmed_pipeline.utils.azure_llm import get_client_and_embed_model
from pubmed_pipeline.utils.log_config import get_logger

logger = get_logger(__name__)

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

SQLITE_DB = os.path.expanduser(
    "~/pubmed_pipeline/pubmed_pipeline/data/storage/pubmed_etl.db"
)

CHUNK_SIZE = 700
CHUNK_OVERLAP = 120


# ---------------------------------------------------------
# 1. Load papers
# ---------------------------------------------------------

def load_papers() -> List[Tuple[str, str]]:
    logger.info("Loading papers from SQLite (pmid + abstract)…")

    if not os.path.exists(SQLITE_DB):
        logger.error(f"SQLite file not found: {SQLITE_DB}")
        return []

    conn = sqlite3.connect(SQLITE_DB)
    cur = conn.cursor()

    try:
        cur.execute("SELECT pmid, abstract FROM papers WHERE abstract IS NOT NULL;")
        rows = cur.fetchall()
    except Exception as e:
        logger.exception(f"SQLite query failed: {e}")
        rows = []

    conn.close()

    logger.info(f"Found {len(rows)} abstracts.")
    return rows


# ---------------------------------------------------------
# 2. Chunk text
# ---------------------------------------------------------

def chunk_text(text: str) -> List[str]:
    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


# ---------------------------------------------------------
# 3. Ingest chunks + embeddings into PGVector
# ---------------------------------------------------------

def load_to_pg(papers: List[Tuple[str, str]]):
    logger.info("Uploading embeddings + chunks to Azure PostgreSQL…")

    # Azure OpenAI embedding client
    client, embed_model = get_client_and_embed_model()

    # PostgreSQL connection
    try:
        conn = psycopg2.connect(
            host=os.getenv("PG_HOST"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
            dbname=os.getenv("PG_DB"),          # <--- FIXED
            port=os.getenv("PG_PORT", "5432"),
            sslmode="require",
        )
        cur = conn.cursor()
    except Exception as e:
        logger.exception(f"PostgreSQL connection failed: {e}")
        return

    insert_sql = """
        INSERT INTO pubmed_chunks (pmid, chunk_id, text, embedding)
        VALUES (%s, %s, %s, %s);
    """

    for pmid, abstract in papers:
        chunks = chunk_text(abstract)

        for idx, chunk in enumerate(chunks):
            try:
                # Compute embedding
                emb = client.embeddings.create(
                    model=embed_model,
                    input=chunk
                ).data[0].embedding

                # Insert row into PGVector table
                cur.execute(insert_sql, (pmid, idx, chunk, emb))

            except Exception as e:
                logger.exception(f"Failed on pmid={pmid}, chunk={idx}: {e}")

    conn.commit()
    cur.close()
    conn.close()

    logger.info("Ingestion completed successfully.")


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():
    papers = load_papers()
    if not papers:
        logger.error("No papers found — ingestion aborted.")
        return

    load_to_pg(papers)


if __name__ == "__main__":
    main()
