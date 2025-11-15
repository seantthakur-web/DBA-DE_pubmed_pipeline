from pubmed_pipeline.utils.azure_llm import get_client_and_chat_model
from pubmed_pipeline.utils.log_config import get_logger

logger = get_logger(__name__)


class RouterAgent:
    def __call__(self, state):
        client, model = get_client_and_chat_model()
        query = state.query

        prompt = f"""
Classify the intent of this biomedical question into exactly one category:
summarize
insight
answer

Return ONLY the label.

Question:
{query}
"""

        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
            )
            intent = resp.choices[0].message.content.strip().lower()
            state.intent = intent
            state.execution_order.append("router")
        except Exception as e:
            logger.exception(f"RouterAgent failed: {e}")
            state.intent = "summarize"
            state.execution_order.append("router_error")

        return state
