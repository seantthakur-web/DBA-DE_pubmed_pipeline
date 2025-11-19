from pubmed_pipeline.agents.base.shared import AgentState
from pubmed_pipeline.rag.rag_retriever import retrieve_docs
from pubmed_pipeline.utils.log_config import get_logger

logger = get_logger(__name__)


class RouterAgent:
    """
    RouterAgent (Production – INNVO-500)

    Responsibilities:
    - Determine intent (currently always "answer")
    - Call real PGVector retriever
    - Populate state.retrieved_docs with real documents
    - Append "router" to execution_order
    """

    def run(self, state: AgentState) -> AgentState:
        trace_id = state.trace_id
        query = state.query
        top_k = state.top_k if hasattr(state, "top_k") else 5

        logger.info(
            f"[trace_id={trace_id}] RouterAgent: routing to answer + performing retrieval (top_k={top_k})"
        )

        # Ensure execution_order exists
        if getattr(state, "execution_order", None) is None:
            state.execution_order = []
        state.execution_order.append("router")

        # Force answer intent
        state.intent = "answer"

        # ------------------------------------------------------------------
        # Execute REAL PGVector retrieval here
        # ------------------------------------------------------------------
        try:
            docs = retrieve_docs(query, top_k)
            state.retrieved_docs = docs
            logger.info(
                f"[trace_id={trace_id}] RouterAgent: retrieved {len(docs)} documents from PGVector"
            )
        except Exception as e:
            logger.exception(
                f"[trace_id={trace_id}] RouterAgent: retrieval failed: {e}"
            )
            state.retrieved_docs = []

        return state


# LangGraph node wrapper
router_agent_instance = RouterAgent()

def router_node(state: AgentState) -> AgentState:
    return router_agent_instance.run(state)
