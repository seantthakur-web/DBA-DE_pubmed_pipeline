import os
import sys
import json
import time
import logging
from dotenv import load_dotenv
from psycopg2.extras import execute_values

# ✅ ensure utils path is visible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db_connection import get_connection

# ✅ Load environment variables
load_dotenv()
os.makedirs("logs", exist_ok=True)

# ✅ Configure logging
logging.basicConfig(
    filename="logs/llama_listener_azure.out",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# ✅ Azure OpenAI client
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-02-01",
)
MODEL_NAME = os.getenv("MODEL_NAME", "embeddings")

# ------------------------------------------------------------
# 🔹 Helper functions
# ------------------------------------------------------------

def get_embedding(text: str, retries: int = 3, delay: float = 2.0):
    """Generate embeddings using Azure OpenAI with retry logic."""
    for attempt in range(1, retries + 1):
        try:
            response = client.embeddings.create(model=MODEL_NAME, input=text)
            return response.data[0].embedding
        except Exception as e:
            logging.warning(f"[Attempt {attempt}/{retries}] Embedding failed: {e}")
            time.sleep(delay)
    raise RuntimeError("❌ Failed to generate embedding after multiple attempts")

def insert_embeddings(records):
    """Insert generated embeddings into PostgreSQL."""
    conn = get_connection()
    cur = conn.cursor()
    sql = """
        INSERT INTO pubmed_vectors (pmid, title, abstract, embedding)
        VALUES %s
    """
    data = [
        (r["pmid"], r["title"], r["abstract"], r["embedding"])
        for r in records
    ]
    execute_values(cur, sql, data)
    conn.commit()
    cur.close()
    conn.close()

def process_message(message):
    """Prepare the record and generate its embedding."""
    pmid = message.get("pmid")
    title = message.get("title", "")
    abstract = message.get("abstract", "")
    text = f"{title}. {abstract}"
    emb = get_embedding(text)
    return {"pmid": pmid, "title": title, "abstract": abstract, "embedding": emb}

# ------------------------------------------------------------
# 🔹 Main listener loop
# ------------------------------------------------------------
if __name__ == "__main__":
    print("🚀 Azure OpenAI listener started (LLaMA/Mistral → PGVector)")
    logging.info("Listener started for Azure OpenAI embeddings.")
    print("Paste PubMed JSON record (or 'q' to quit):")

    while True:
        msg = input("> ").strip()
        if msg.lower() == "q":
            print("👋 Exiting listener...")
            logging.info("Listener stopped manually.")
            break
        try:
            m = json.loads(msg)
            rec = process_message(m)
            insert_embeddings([rec])
            print(f"✅ Inserted embedding for PMID {rec['pmid']}")
            logging.info(f"✅ Inserted embedding for PMID {rec['pmid']}")
        except Exception as e:
            print(f"❌ Error: {e}")
            logging.error(f"❌ Error processing message: {e}")

