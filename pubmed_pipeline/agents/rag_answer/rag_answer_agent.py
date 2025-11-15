from pubmed_pipeline.utils.azure_llm import get_client_and_chat_model
from pubmed_pipeline.utils.log_config import get_logger

logger = get_logger(__name__)


class RAGAnswerAgent:
    def __call__(self, state):
        client, model = get_client_and_chat_model()

        query = state.query
        summaries = state.summaries or ""
        insights = state.insights or []
        docs = state.retrieved_docs or []

        citations = "\n".join([
            f"- PMID {d['pmid']} (chunk {d['chunk_id']})"
            for d in docs
        ])

        prompt = f"""
Provide a biomedical answer grounded ONLY in the following evidence.

Question:
{query}

Summary:
{summaries}

Insights:
{insights}

Citations:
{citations}
"""

        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
            )
            state.final_answer = resp.choices[0].message.content.strip()
            state.used_llm = True
            state.execution_order.append("rag_answer")
        except Exception as e:
            logger.exception(f"RAGAnswerAgent error: {e}")
            state.final_answer = "Final answer could not be generated."
            state.used_llm = False
            state.execution_order.append("rag_answer_error")

        return state
