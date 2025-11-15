from pubmed_pipeline.utils.azure_llm import get_client_and_chat_model
from pubmed_pipeline.utils.log_config import get_logger

logger = get_logger(__name__)


class SummarizerAgent:
    def __call__(self, state):
        client, model = get_client_and_chat_model()
        docs = state.retrieved_docs or []

        if not docs:
            state.summaries = None
            return state

        evidence = "\n\n".join([d["text"] for d in docs])

        prompt = f"Summarize the following biomedical evidence:\n\n{evidence}"

        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
            )
            summary = resp.choices[0].message.content.strip()
            state.summaries = summary
            state.execution_order.append("summarizer")
        except Exception as e:
            logger.exception(f"SummarizerAgent error: {e}")
            state.summaries = None
            state.execution_order.append("summarizer_error")

        return state
