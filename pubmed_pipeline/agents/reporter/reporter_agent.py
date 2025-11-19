from pubmed_pipeline.utils.azure_llm import get_client_and_chat_model
from pubmed_pipeline.utils.log_config import get_logger
from pubmed_pipeline.agents.base.shared import AgentState

logger = get_logger(__name__)


class ReporterAgent:
    """
    ReporterAgent

    Responsibilities:
    - Consume state.summaries
    - Extract 3–5 biomedical insights
    - Populate state.insights
    - Append 'reporter' to execution_order
    """

    def __init__(self):
        self.client, self.model = get_client_and_chat_model()

    def run(self, state: AgentState) -> AgentState:
        trace_id = state.trace_id
        logger.info(f"[trace_id={trace_id}] ReporterAgent: extracting insights")

        # Ensure execution_order exists
        if getattr(state, "execution_order", None) is None:
            state.execution_order = []

        state.execution_order.append("reporter")

        summaries = state.summaries or []

        # No summaries → fallback
        if not summaries:
            state.insights = ["No summaries available to extract insights from."]
            return state

        combined_summary = "\n".join(summaries)

        prompt = f"""
Extract 3–5 high-value biomedical insights from the summary below.
Return ONLY bullet points (e.g., "- Insight"), no prose.

Summary:
\"\"\"{combined_summary}\"\"\"
"""

        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=350,
            )

            raw = resp.choices[0].message.content or ""

            insights = [
                line.lstrip("-• ").strip()
                for line in raw.splitlines()
                if line.strip()
            ]

            if not insights:
                insights = ["No stable insights extracted."]

            state.insights = insights

        except Exception as e:
            logger.exception(
                f"[trace_id={trace_id}] ReporterAgent: LLM error: {e}"
            )
            state.insights = ["Insight extraction temporarily unavailable."]
            state.execution_order.append("reporter_error")

        return state


# ===========================================================
# LangGraph-Compatible Node Wrapper
# ===========================================================

reporter_agent_instance = ReporterAgent()

def reporter_node(state: AgentState) -> AgentState:
    """
    LangGraph-compatible node wrapper for ReporterAgent.
    """
    return reporter_agent_instance.run(state)
