from fastapi import APIRouter, HTTPException
from api.schemas import ArtifactResponse
from utils.artifact_writer import ARTIFACT_DIR
import json

router = APIRouter()


@router.get("/{trace_id}", response_model=ArtifactResponse)
async def get_artifact(trace_id: str):
    matches = list(ARTIFACT_DIR.glob(f"*{trace_id}.json"))

    if not matches:
        raise HTTPException(status_code=404, detail="Artifact not found")

    path = matches[0]
    with open(path, "r") as f:
        content = json.load(f)

    return ArtifactResponse(trace_id=trace_id, content=content)
