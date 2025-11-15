from pubmed_pipeline.utils.azure_llm import get_client_and_chat_model
from pubmed_pipeline.utils.log_config import get_logger

logger = get_logger(__name__)


class ReporterAgent:
    def __call__(self, state):
        client, model = get_client_and_chat_model()
        docs = state.retrieved_docs or []

        if not docs:
            state.insights = ["No evidence available"]
            return state

        evidence = "\n\n".join([d["text"] for d in docs])

        prompt = f"""
Extract 3–5 key biomedical insights from the evidence.
Return as bullet points.

{evidence}
"""

        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = resp.choices[0].message.content

            insights = [
                line.lstrip("-• ").strip()
                for line in raw.splitlines()
                if line.strip()
            ]

            state.insights = insights
            state.execution_order.append("reporter")
        except Exception as e:
            logger.exception(f"ReporterAgent error: {e}")
            state.insights = ["Insight extraction failed."]
            state.execution_order.append("reporter_error")

        return state
