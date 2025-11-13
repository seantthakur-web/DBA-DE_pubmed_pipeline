from fastapi import APIRouter, HTTPException
from agents.dag_controller import DAGController
from utils.log_config import get_logger
from utils.artifact_writer import ARTIFACT_DIR
from api.schemas import WorkflowRequest, WorkflowResponse, WorkflowListResponse

import json
from pathlib import Path

router = APIRouter()
logger = get_logger("workflow_api")

controller = DAGController()


@router.get("/list", response_model=WorkflowListResponse)
async def list_workflows():
    workflows = list(controller.workflows.keys())
    return WorkflowListResponse(workflows=workflows)


@router.post("/run", response_model=WorkflowResponse)
async def run_workflow(request: WorkflowRequest):
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    workflow_name = request.workflow_name
    if workflow_name not in controller.workflows:
        raise HTTPException(status_code=400, detail=f"Unknown workflow: {workflow_name}")

    logger.info(f"Running workflow '{workflow_name}' for query='{query}'")

    initial_state = {"query": query}
    final_state = controller.run_workflow(workflow_name, initial_state)

    # Convert state to dict
    final_dict = final_state.model_dump()

    # Determine saved artifact path
    trace_id = final_dict["trace_id"]
    artifact_path = next((str(p) for p in ARTIFACT_DIR.glob(f"*{trace_id}.json")), None)

    return WorkflowResponse(
        trace_id=trace_id,
        query=final_dict["query"],
        summary=final_dict.get("summary"),
        answer=final_dict.get("answer"),
        insights=final_dict.get("insights"),
        retrieved_docs=final_dict.get("retrieved_docs"),
        debug=final_dict.get("debug", {}),
        artifact_path=artifact_path
    )
