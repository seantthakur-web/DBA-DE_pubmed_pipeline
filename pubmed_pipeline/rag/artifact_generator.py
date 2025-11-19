import json
import os
from datetime import datetime
from typing import Any

ARTIFACT_DIR = "pubmed_pipeline/data/artifacts"


def save_artifact(response: Any) -> str:
    """
    Saves an API response object (e.g., AskResponse) as a JSON artifact.

    This function is intentionally decoupled from FastAPI schemas to avoid
    circular imports. It uses duck-typing:
      - Tries response.model_dump()
      - Falls back to dict(response)
    """

    os.makedirs(ARTIFACT_DIR, exist_ok=True)

    # Try to extract data from Pydantic/BaseModel-like object
    if hasattr(response, "model_dump"):
        data = response.model_dump()
    elif isinstance(response, dict):
        data = dict(response)
    else:
        # Last-resort: try to coerce to dict
        try:
            data = dict(response)
        except Exception:
            raise TypeError(
                f"save_artifact expected a Pydantic model or dict-like object, got: {type(response)}"
            )

    trace_id = data.get("trace_id", "unknown-trace")

    filename = f"artifact_{trace_id}.json"
    path = os.path.join(ARTIFACT_DIR, filename)

    data["_artifact_created_at"] = datetime.utcnow().isoformat()

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    return path
