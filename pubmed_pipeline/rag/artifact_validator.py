import json
import os
from typing import List

REQUIRED_TOP_LEVEL_FIELDS = [
    "trace_id",
    "query",
    "intent",
    "execution_order",
    "summaries",
    "insights",
    "retrieved_docs",
    "final_answer",
]

REQUIRED_RETRIEVED_DOC_FIELDS = [
    "pmid",
    "chunk_id",
    "text",
]


def validate_artifact(path: str) -> List[str]:
    """
    Validates a JSON artifact. Returns list of errors (empty list = valid).
    """

    errors = []

    if not os.path.exists(path):
        return [f"File does not exist: {path}"]

    try:
        with open(path, "r") as f:
            data = json.load(f)
    except Exception as e:
        return [f"Invalid JSON: {e}"]

    # Validate required fields
    for field in REQUIRED_TOP_LEVEL_FIELDS:
        if field not in data:
            errors.append(f"Missing field: {field}")

    # Validate retrieved_docs structure
    for doc in data.get("retrieved_docs", []):
        for f in REQUIRED_RETRIEVED_DOC_FIELDS:
            if f not in doc:
                errors.append(f"Document missing field '{f}' in retrieved_docs")

    return errors
