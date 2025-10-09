# etl/manifest_tracker.py
import os, json
from datetime import datetime

MANIFEST_PATH = "data/logs/etl_manifest.json"

def update_manifest(filename):
    os.makedirs(os.path.dirname(MANIFEST_PATH), exist_ok=True)
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, "r") as f:
            manifest = json.load(f)
    else:
        manifest = {"processed": []}

    manifest["processed"].append({
        "filename": filename,
        "timestamp": datetime.now().isoformat()
    })

    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)
