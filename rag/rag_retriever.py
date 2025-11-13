import psycopg2
from psycopg2.extras import RealDictCursor
from pubmed_pipeline.utils.keyvault_client import get_secret
from pubmed_pipeline.utils.log_config import get_logger
import json
import os

# ---------------------------------------------------------------------------
# PubMed RAG Retriever  – INNVO-493 (aligned with INNVO-490 centralized logging)
# ---------------------------------------------------------------------------

logger = get_logger(__name__)

def get_db_connection():
    """
    Establish connection to Azure PostgreSQL (pgvector enabled).
    Secrets are fetched securely from Azure Key Vault.
    """
    try:
        conn = psycopg2.connect(
            host=get_secret("PGHOST"),
            user=get_secret("PGUSER"),
            password=get_secret("PGPASSWORD"),
            dbname=get_secret("PGDATABASE"),
            connect_timeout=10,
        )
        logger.info("✅ Database connection established.")
        return conn
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}", exc_info=True)
        raise


def retrieve_docs(query: str, top_k: int = 3):
    """
    Retrieves top-K most similar PubMed documents from pgvector table.
    """
    logger.info(f"➡️ Retrieving top {top_k} results for query: '{query}'")

    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        sql = """
        SELECT pmid, title, abstract, similarity
        FROM pubmed_vectors
        ORDER BY similarity DESC
        LIMIT %s;
        """
        cur.execute(sql, (top_k,))
        rows = cur.fetchall()
        conn.close()

        logger.info(f"✅ Retrieved {len(rows)} rows successfully.")
        return rows

    except Exception as e:
        logger.error(f"⚠️ Retrieval failed: {e}", exc_info=True)
        return []


# ---------------------------------------------------------------------------
# CLI test:  python3 -m pubmed_pipeline.rag.rag_retriever
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_query = "cisplatin S-1 gastric cancer outcomes"
    logger.info("🧩 Running retriever self-test.")
    results = retrieve_docs(test_query, top_k=3)
    print(json.dumps(results, indent=2))
    logger.info("🏁 Retriever self-test completed.")
    print(
        f"✅ Log entries written to: "
        f"{os.path.expanduser('~/pubmed_pipeline/data/logs/rag_pipeline/rag.log')}"
    )
