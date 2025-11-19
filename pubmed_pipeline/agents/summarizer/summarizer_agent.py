from typing import List
from textwrap import shorten

from pubmed_pipeline.agents.base.shared import AgentState
from pubmed_pipeline.utils.log_config import get_logger
from pubmed_pipeline.utils.azure_llm import get_client_and_chat_model

logger = get_logger(__name__)

MAX_DOCS_FOR_SUMMARY = 8
MAX_EVIDENCE_CHARS = 2000


class SummarizerAgent:
    """
    Production-grade biomedical summarization agent.

    Responsibilities:
    - Consume state.retrieved_docs
    - Produce hybrid-format summaries:
        Key Findings:
        - ...
        
        Clinical Interpretation:
        ...
    - Write to state.summaries
    - Append "summarizer" to execution_order
    """

    def __init__(self):
        self.client, self.model = get_client_and_chat_model()

    def run(self, state: AgentState) -> AgentState:
        trace_id = state.trace_id
        logger.info(
            "[trace_id=%s] SummarizerAgent: summarizing %d docs",
            trace_id,
            len(state.retrieved_docs),
        )

        # Track execution
        if getattr(state, "execution_order", None) is None:
            state.execution_order = []
        state.execution_order.append("summarizer")

        docs = state.retrieved_docs or []

        # ----------------------------
        # No evidence → fallback
        # ----------------------------
        if not docs:
            logger.warning(
                "[trace_id=%s] SummarizerAgent: no retrieved_docs found",
                trace_id,
            )
            state.summaries = [
                "Key Findings:\n"
                "- No biomedical evidence retrieved.\n\n"
                "Clinical Interpretation:\n"
                "Insufficient evidence to generate a meaningful summary."
            ]
            return state

        # Build evidence block for LLM prompt
        evidence_block = self._build_evidence_block(docs)
        prompt = self._build_prompt(state.query, evidence_block)

        # ----------------------------
        # LLM CALL
        # ----------------------------
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=450,
            )

            summary_text = (resp.choices[0].message.content or "").strip()

        except Exception as e:
            logger.exception(
                "[trace_id=%s] SummarizerAgent: LLM call failed: %s",
                trace_id, e
            )
            state.summaries = [
                "Key Findings:\n"
                "- Summarization failed due to internal error.\n\n"
                "Clinical Interpretation:\n"
                "Retry the request or contact the system owner."
            ]
            return state

        # Empty output fallback
        if not summary_text:
            logger.warning(
                "[trace_id=%s] SummarizerAgent: empty output",
                trace_id,
            )
            state.summaries = [
                "Key Findings:\n"
                "- No content returned by the LLM.\n\n"
                "Clinical Interpretation:\n"
                "No summary could be generated from evidence."
            ]
        else:
            state.summaries = [summary_text]

        logger.info(
            "[trace_id=%s] SummarizerAgent: completed, produced %d summaries",
            trace_id,
            len(state.summaries),
        )

        return state

    # ------------------------------------------------------------------
    # INTERNAL HELPERS
    # ------------------------------------------------------------------

    def _build_evidence_block(self, docs: List[dict]) -> str:
        lines = []
        selected = docs[:MAX_DOCS_FOR_SUMMARY]

        for idx, d in enumerate(selected, start=1):
            pmid = d.get("pmid", "UNKNOWN")
            text = (
                d.get("text")
                or d.get("chunk_text")
                or d.get("content")
                or ""
            ).replace("\n", " ").strip()

            snippet = shorten(text, width=MAX_EVIDENCE_CHARS, placeholder="…")
            lines.append(f"[{idx}] PMID {pmid}:\n{snippet}\n")

        return "\n".join(lines)

    def _build_prompt(self, question: str, evidence_block: str) -> str:
        return f"""
You are a biomedical summarization agent working over retrieved PubMed evidence.

User question:
\"\"\"{question}\"\"\"

Evidence:
{evidence_block}

Write a hybrid-format summary in this EXACT structure:

Key Findings:
- Bullet 1 (concise and grounded in evidence)
- Bullet 2
- Bullet 3
(up to 5 total bullets)

Clinical Interpretation:
2–4 sentence paragraph explaining the meaning of the findings,
including mechanisms, implications, or limitations.

Rules:
- Do NOT hallucinate new drugs, genes, PMIDs, or outcomes.
- Use ONLY the evidence above.
- Do NOT include inline citations like [1] or PMID numbers.
- Write clearly for a clinician reader.
""".strip()


# ============================================
# LangGraph-Compatible Node Callable
# ============================================

summarizer_agent_instance = SummarizerAgent()

def summarizer_node(state: AgentState) -> AgentState:
    """
    LangGraph-compatible node wrapper.
    """
    return summarizer_agent_instance.run(state)
