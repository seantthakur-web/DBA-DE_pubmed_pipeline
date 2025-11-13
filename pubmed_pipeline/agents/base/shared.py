"""
shared.py
Provides:
- Global logger
- AgentState (lightweight dict wrapper)
- Node timing utilities
"""

from __future__ import annotations
import logging
import time
import uuid


# ----------------------------------------------------------------------
# LOGGER
# ----------------------------------------------------------------------
logger = logging.getLogger("pubmed_pipeline")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    )
    logger.addHandler(handler)


# ----------------------------------------------------------------------
# AgentState: minimal dict-like container used by all agents
# ----------------------------------------------------------------------
class AgentState(dict):
    """
    Minimal state container for LangGraph agents.
    Behaves like a dict but provides a cleaner semantic meaning.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "trace_id" not in self:
            self["trace_id"] = str(uuid.uuid4())

    # optional helper
    def append_node(self, name: str):
        self.setdefault("node_sequence", []).append(name)


# ----------------------------------------------------------------------
# Node timing utilities (agents call these)
# ----------------------------------------------------------------------
def mark_node_start(state: dict, node_name: str) -> None:
    state.setdefault("node_sequence", []).append(node_name)
    state.setdefault("timestamps", {})[f"{node_name}_start"] = time.time()


def mark_node_end(state: dict, node_name: str) -> None:
    state.setdefault("timestamps", {})[f"{node_name}_end"] = time.time()
