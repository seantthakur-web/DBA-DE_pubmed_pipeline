import os
import psycopg2
from dotenv import load_dotenv
from pubmed_pipeline.utils.log_config import get_logger

logger = get_logger(__name__)

# Load .env explicitly
load_dotenv("/home/seanthakur/pubmed_pipeline/.env")

def get_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("PG_HOST"),
            dbname=os.getenv("PG_DATABASE"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
            port=os.getenv("PG_PORT"),
            sslmode="require"
        )
        return conn
    except Exception as e:
        logger.error(f"PG connection failed: {e}")
        raise

