import yaml
import logging
import uuid
from pathlib import Path
from typing import Dict, Any

from agents.base.shared import AgentState
from agents.router.router_agent import RouterAgent
from agents.summarizer.summarizer_agent import SummarizerAgent
from agents.reporter.reporter_agent import ReporterAgent
from agents.rag_answer.rag_answer_agent import RAGAnswerAgent

# INNVO-503 artifact writer
from utils.artifact_writer import save_artifact

logger = logging.getLogger(__name__)


# Agent registry for dynamic dispatch
AGENT_MAP = {
    "router": RouterAgent,
    "summarizer": SummarizerAgent,
    "reporter": ReporterAgent,
    "rag_answer": RAGAnswerAgent,
}


WORKFLOW_CONFIG_PATH = (
    Path(__file__).resolve().parents[1] / "configs" / "workflows.yaml"
)


class DAGController:
    """
    Dynamic workflow executor for a LangGraph-like DAG.
    Loads node graph from workflows.yaml and executes agents in sequence.
    """

    def __init__(self):
        self.workflows = self._load_workflows()

    # ---------------------------------------------------------
    # Load workflow definitions
    # ---------------------------------------------------------
    def _load_workflows(self) -> Dict[str, Any]:
        if not WORKFLOW_CONFIG_PATH.exists():
            raise FileNotFoundError(
                f"Missing workflows.yaml at: {WORKFLOW_CONFIG_PATH}"
            )

        with open(WORKFLOW_CONFIG_PATH, "r") as f:
            data = yaml.safe_load(f)

        logger.info(f"Loaded workflow definitions: {list(data.keys())}")
        return data

    # ---------------------------------------------------------
    # Ensure the state is an AgentState object
    # ---------------------------------------------------------
    def _ensure_agent_state(self, state: Any) -> AgentState:
        if isinstance(state, AgentState):
            return state
        if isinstance(state, dict):
            return AgentState(**state)
        raise TypeError(f"State must be AgentState or dict, got: {type(state)}")

    # ---------------------------------------------------------
    # Run a workflow end-to-end
    # ---------------------------------------------------------
    def run_workflow(self, workflow_name: str, state: Dict[str, Any]) -> AgentState:
        workflow = self.workflows.get(workflow_name)
        if not workflow:
            raise ValueError(f"Workflow '{workflow_name}' not found in workflows.yaml")

        # Convert dict → model
        state = self._ensure_agent_state(state)

        # Assign trace ID for entire run
        trace_id = str(uuid.uuid4())
        state.trace_id = trace_id
        logger.info(f"[trace_id={trace_id}] Starting workflow: {workflow_name}")

        nodes = workflow["nodes"]
        entry_node = workflow["entry"]
        exit_nodes = workflow["exit"]

        current = entry_node

        # Iterate until we hit an exit node
        while True:
            node_cfg = nodes[current]
            agent_name = node_cfg["agent"]
            retries = node_cfg.get("retries", 1)

            # Run this step
            state = self._run_agent_step(agent_name, state, retries, trace_id)

            # Compute next node
            next_step = self._get_next_step(workflow, current, state)
            logger.info(
                f"[trace_id={trace_id}] Current node: {current} → Next: {next_step}"
            )

            # If next node is exit node: run AND finish
            if next_step in exit_nodes:
                final_cfg = nodes[next_step]
                final_agent = final_cfg["agent"]

                state = self._run_agent_step(
                    final_agent, state, 1, trace_id
                )

                logger.info(
                    f"[trace_id={trace_id}] Workflow reached exit node: {next_step}"
                )

                # INNVO-503: Save final artifact
                payload = state.model_dump()
                artifact_path = save_artifact(trace_id, payload)
                logger.info(f"[trace_id={trace_id}] Saved output artifact → {artifact_path}")

                return state

            # Continue to next node
            current = next_step

    # ---------------------------------------------------------
    # Execute agent logic w/ retry support
    # ---------------------------------------------------------
    def _run_agent_step(
        self, agent_name: str, state: AgentState, retries: int, trace_id: str
    ) -> AgentState:

        if agent_name not in AGENT_MAP:
            raise ValueError(f"Unknown agent '{agent_name}'")

        agent_cls = AGENT_MAP[agent_name]
        agent = agent_cls()

        attempt = 1
        while attempt <= retries:
            try:
                logger.info(
                    f"[trace_id={trace_id}] → Executing '{agent_name}' (Attempt {attempt}/{retries})"
                )
                return agent.run(state)

            except Exception as e:
                logger.error(
                    f"[trace_id={trace_id}] Error in node '{agent_name}': {e}"
                )
                attempt += 1

                if attempt > retries:
                    logger.error(
                        f"[trace_id={trace_id}] Maximum retries reached for '{agent_name}'"
                    )
                    raise

    # ---------------------------------------------------------
    # Determine next step (supports override logic)
    # ---------------------------------------------------------
    def _get_next_step(
        self,
        workflow: Dict[str, Any],
        current: str,
        state: AgentState,
    ) -> str:
        """Allow custom routing between nodes."""

        # Example override: user may skip reporter
        if current == "summarizer" and getattr(state, "skip_reporter", False):
            return "rag_answer"

        return workflow["nodes"][current]["next"]

