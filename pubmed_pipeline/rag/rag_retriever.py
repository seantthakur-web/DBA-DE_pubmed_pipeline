import os
import psycopg2
from typing import List, Dict, Any

from pubmed_pipeline.utils.azure_llm import get_client_and_embed_model
from pubmed_pipeline.utils.log_config import get_logger

logger = get_logger(__name__)


def get_pg_connection():
    """Return a psycopg2 connection using environment variables."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT", 5432),
            dbname=os.getenv("PG_DATABASE"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
            sslmode="require"
        )
        return conn
    except Exception as e:
        logger.exception(f"PG connection failed: {e}")
        raise


def retrieve_docs(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Embed query -> perform cosine distance search using PGVector.
    """
    client, embed_model = get_client_and_embed_model()

    # 1. Generate embedding
    try:
        emb = client.embeddings.create(
            model=embed_model,
            input=query
        ).data[0].embedding
    except Exception as e:
        logger.exception(f"Embedding generation failed: {e}")
        return []

    # 2. Connect to PostgreSQL
    try:
        conn = get_pg_connection()
        cur = conn.cursor()
    except Exception:
        return []

    # 3. Run vector search
    sql = """
        SELECT pmid, chunk_id, text,
               1 - (embedding <=> %s::vector) AS score
        FROM pubmed_chunks
        ORDER BY embedding <=> %s::vector
        LIMIT %s;
    """

    try:
        cur.execute(sql, (emb, emb, top_k))
        rows = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        logger.exception(f"PGVector query failed: {e}")
        return []

    # 4. Return results
    return [
        {
            "pmid": r[0],
            "chunk_id": r[1],
            "text": r[2],
            "score": float(r[3]),
        }
        for r in rows
    ]
