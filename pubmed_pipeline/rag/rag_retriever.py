import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

from pubmed_pipeline.utils.log_config import get_logger
from pubmed_pipeline.utils.azure_llm import embed_text
from pubmed_pipeline.utils.db_connection import get_connection

logger = get_logger(__name__)

# Load .env explicitly
ENV_PATH = "/home/seanthakur/pubmed_pipeline/.env"
if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)
    logger.info(f"Loaded .env from {ENV_PATH}")
else:
    logger.error(f"Missing .env file at {ENV_PATH}")


# ------------------------------------------------------------------------------------
# Convert Python embedding array → pgvector literal '[0.1, 0.2, ...]'
# ------------------------------------------------------------------------------------
def _to_pgvector_literal(embedding):
    return "[" + ",".join(str(x) for x in embedding) + "]"


# ------------------------------------------------------------------------------------
# Run pgvector similarity search
# ------------------------------------------------------------------------------------
def _vector_search(conn, embedding, top_k):
    vector_literal = _to_pgvector_literal(embedding)

    sql = """
        SELECT 
            pmid,
            chunk_id,
            text,
            1 - (embedding <=> %s::vector) AS score
        FROM pubmed_chunks
        ORDER BY embedding <=> %s::vector
        LIMIT %s;
    """

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (vector_literal, vector_literal, top_k))
            rows = cur.fetchall()
            return rows

    except Exception as e:
        logger.error(f"Vector search failed: {e}")
        raise


# ------------------------------------------------------------------------------------
# Main retrieval function (public)
# ------------------------------------------------------------------------------------
def retrieve_docs(query: str, top_k: int = 5):
    logger.info(f"RAG retriever: querying pgvector | query='{query}' | top_k={top_k}")

    # ----------------------------------------------------
    # 1. Embed the query
    # ----------------------------------------------------
    try:
        embedding = embed_text(query)
        logger.info(f"Obtained embedding of length {len(embedding)}")
    except Exception as e:
        logger.error(f"Embedding failed: {e}")
        return []

    # ----------------------------------------------------
    # 2. PGVector search
    # ----------------------------------------------------
    try:
        conn = get_connection()
    except Exception as e:
        logger.error(f"PG connection failed: {e}")
        return []

    try:
        rows = _vector_search(conn, embedding, top_k)
        results = []

        for r in rows:
            results.append({
                "pmid": r["pmid"],
                "chunk_id": r["chunk_id"],
                "text": r["text"],
                "score": float(r["score"]),
            })

        conn.close()
        return results

    except Exception as e:
        logger.error(f"RAG retriever: vector search error: {e}")
        return []
