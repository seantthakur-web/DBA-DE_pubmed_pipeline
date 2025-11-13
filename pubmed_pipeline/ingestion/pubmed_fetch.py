import os
import json
import time
from dotenv import load_dotenv
from Bio import Entrez
from kafka_stub import publish_to_local_stream  # <-- local stub publisher

# --- Load environment variables from .env ---
load_dotenv()
Entrez.email = os.getenv("ENTREZ_EMAIL", "your_email@domain.com")
Entrez.api_key = os.getenv("ENTREZ_API_KEY")

# --- Define data folders ---
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
STREAM_DIR = os.path.join(BASE_DIR, "data", "streaming")

# --- Ensure directories exist ---
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(STREAM_DIR, exist_ok=True)


def fetch_pubmed(query="gastric cancer AND nutrition", retmax=20):
    """
    Fetch PubMed abstracts, save locally in /data/raw,
    and simulate Kafka streaming via /data/streaming.
    """
    print(f"🔍 Searching PubMed for: {query}")
    handle = Entrez.esearch(db="pubmed", term=query, retmax=retmax, sort="relevance")
    record = Entrez.read(handle)
    pmids = record.get("IdList", [])
    print(f"Found {len(pmids)} results.")

    if not pmids:
        print("No results found.")
        return

    # Fetch full records from PubMed
    fetch_handle = Entrez.efetch(db="pubmed", id=",".join(pmids), rettype="xml")
    articles = Entrez.read(fetch_handle)["PubmedArticle"]

    for art in articles:
        pmid = art["MedlineCitation"]["PMID"]
        raw_path = os.path.join(RAW_DIR, f"{pmid}.json")

        # Save locally
        with open(raw_path, "w", encoding="utf-8") as f:
            json.dump(art, f, indent=2)

        # Simulated Kafka publish (writes to /data/streaming)
        publish_to_local_stream(art)

        print(f"💾 Saved + 📤 Streamed (simulated) {pmid}")
        time.sleep(0.3)  # Respect NCBI rate limits

    print("✅ Ingestion complete!")


if __name__ == "__main__":
    fetch_pubmed()
