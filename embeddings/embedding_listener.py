# ==========================================================
# INNVO-418 – LLaMA / Mistral Embedding Integration
# ==========================================================
import os, json, psycopg2, requests
from dotenv import load_dotenv

# ----------------------------------------------------------
# Load environment variables
# ----------------------------------------------------------
load_dotenv()

# ----------------------------------------------------------
# Database connection
# ----------------------------------------------------------
conn = psycopg2.connect(os.getenv("POSTGRES_CONN_STRING"))
cursor = conn.cursor()
print("✅ Connected to PostgreSQL")

# ----------------------------------------------------------
# Helper functions
# ----------------------------------------------------------
def fetch_unembedded(limit=5):
    """Fetch records that don’t yet have embeddings."""
    cursor.execute("SELECT pmid, text FROM pubmed_vectors WHERE embedding IS NULL LIMIT %s;", (limit,))
    return cursor.fetchall()

def generate_embedding(text):
    """Generate embedding using Mistral API."""
    headers = {"Authorization": f"Bearer {os.getenv('EMBEDDING_KEY')}"}
    data = {"model": os.getenv("EMBEDDING_MODEL"), "input": text}
    r = requests.post(os.getenv("EMBEDDING_ENDPOINT"), headers=headers, json=data, timeout=60)
    r.raise_for_status()
    return r.json()["data"][0]["embedding"]

def upsert_embedding(pmid, emb):
    """Insert or update embedding in Postgres."""
    cursor.execute("""
        INSERT INTO pubmed_vectors (pmid, embedding)
        VALUES (%s, %s)
        ON CONFLICT (pmid) DO UPDATE SET embedding = EXCLUDED.embedding;
    """, (pmid, emb))
    conn.commit()

# ----------------------------------------------------------
# Main process
# ----------------------------------------------------------
records = fetch_unembedded(5)
print(f"🔹 Found {len(records)} records needing embeddings.")

for pmid, text in records:
    try:
        emb = generate_embedding(text)
        upsert_embedding(pmid, emb)
        print(f"✅ Upsert complete for {pmid}")
    except Exception as e:
        print(f"⚠️ {pmid}: {e}")

cursor.close()
conn.close()
print("🏁 All done.")
