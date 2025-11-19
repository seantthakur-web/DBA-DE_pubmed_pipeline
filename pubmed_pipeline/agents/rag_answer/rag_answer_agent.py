from typing import List, Dict, Any, Optional

from pubmed_pipeline.agents.base.shared import AgentState
from pubmed_pipeline.utils.azure_llm import get_client_and_chat_model
from pubmed_pipeline.utils.log_config import get_logger

logger = get_logger(__name__)


class RAGAnswerAgent:
    """
    Final-answer generator for LangGraph.

    Uses:
    - state.query
    - state.retrieved_docs
    - state.summaries
    - state.insights

    Produces:
    - final_answer (1–3 paragraphs)
    """

    def __init__(self):
        self.client, self.model = get_client_and_chat_model()

    def run(self, state: AgentState) -> AgentState:
        trace_id = state.trace_id
        logger.info(f"[trace_id={trace_id}] RAGAnswerAgent: generating final answer")

        # Ensure execution_order exists
        if getattr(state, "execution_order", None) is None:
            state.execution_order = []
        state.execution_order.append("rag_answer")

        question = state.query or ""
        summaries = state.summaries or []
        insights = state.insights or []
        docs = state.retrieved_docs or []

        # No docs → fallback
        if not docs:
            logger.warning(
                f"[trace_id={trace_id}] RAGAnswerAgent: no retrieved_docs found"
            )
            state.final_answer = (
                "No grounded biomedical answer can be produced because "
                "no PubMed evidence was retrieved. Consider refining the query."
            )
            return state

        evidence_block = _build_context_snippets(docs)

        prompt = _build_final_answer_prompt(
            question=question,
            summaries=summaries,
            insights=insights,
            evidence_block=evidence_block,
        )

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.15,
                max_tokens=550,
            )

            answer = (completion.choices[0].message.content or "").strip()

        except Exception as e:
            logger.exception(
                f"[trace_id={trace_id}] RAGAnswerAgent: LLM call failed: {e}"
            )
            answer = (
                "An internal error occurred while generating the final answer. "
                "Please try again later."
            )

        if not answer:
            logger.warning(
                f"[trace_id={trace_id}] RAGAnswerAgent: empty answer"
            )
            answer = (
                "The system could not construct a stable biomedical answer "
                "from available evidence."
            )

        state.final_answer = answer
        logger.info(f"[trace_id={trace_id}] RAGAnswerAgent: completed")

        return state


# ---------------------------
# Helper: Build snippet block
# ---------------------------

def _build_context_snippets(docs: List[Dict[str, Any]], max_chars: int = 4000) -> str:
    lines = []
    total = 0

    for d in docs:
        pmid = d.get("pmid", "UNKNOWN")
        chunk_id = d.get("chunk_id", 0)
        text = (d.get("text") or "").replace("\n", " ").strip()

        if not text:
            continue

        snippet = text[:400]
        line = f"PMID {pmid} (chunk {chunk_id}): {snippet}"
        line_len = len(line) + 2

        if total + line_len > max_chars:
            break

        lines.append(line)
        total += line_len

    return "\n\n".join(lines)


# ---------------------------
# Helper: Build final answer prompt
# ---------------------------

def _build_final_answer_prompt(
    question: str,
    summaries: List[str],
    insights: List[str],
    evidence_block: str,
) -> str:

    summaries_text = "\n\n".join(summaries)
    insights_text = "\n".join([f"- {i}" for i in insights])

    return f"""
You are a biomedical RAG agent.

User question:
\"\"\"{question}\"\"\"

Summaries:
{summaries_text}

Insights:
{insights_text}

Evidence snippets:
{evidence_block}

Write a final answer (1–3 short paragraphs) that:
- Uses ONLY the provided evidence
- Explains mechanisms, pathways, outcomes, or limitations
- Avoids hallucinations
- Uses clinician-friendly language
- Acknowledges uncertainty where appropriate

Output: a concise biomedical explanation (no bullets).
""".strip()


# ===========================================================
# LangGraph-Compatible Node Wrapper
# ===========================================================

rag_answer_agent_instance = RAGAnswerAgent()

def rag_answer_node(state: AgentState) -> AgentState:
    """
    LangGraph-compatible node wrapper for RAGAnswerAgent.
    """
    return rag_answer_agent_instance.run(state)
