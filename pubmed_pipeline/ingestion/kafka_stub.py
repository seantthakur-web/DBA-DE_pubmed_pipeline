"""
Kafka Stub Publisher
--------------------
Used when Docker/Kafka cannot be installed locally.

Simulates a Kafka producer by writing each message
to the /data/streaming folder.
"""

import os
import json
from datetime import datetime

# --- Define base folder paths ---
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STREAM_DIR = os.path.join(BASE_DIR, "data", "streaming")

# --- Ensure folder exists ---
os.makedirs(STREAM_DIR, exist_ok=True)


def publish_to_local_stream(article: dict):
    """
    Simulate publishing an article to Kafka by saving
    it as a JSON file under /data/streaming/.
    """
    pmid = article["MedlineCitation"]["PMID"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(STREAM_DIR, f"{pmid}_{timestamp}.json")

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(article, f, indent=2)
        print(f"📤 [STUB] Published {pmid} → data/streaming/")
    except Exception as e:
        print(f"❌ [STUB] Failed to publish {pmid}: {e}")
