import os
import json
import requests
from pubmed_pipeline.utils.keyvault_client import get_secret
from pubmed_pipeline.utils.log_config import get_logger

# ---------------------------------------------------------------------------
# RAG Generator – INNVO-492 (Key Vault + Centralized Logging + Fallback)
# ---------------------------------------------------------------------------

logger = get_logger(__name__)

def _get_secret_with_fallback(primary: str, fallback: str):
    """Try both the primary and fallback secret names."""
    try:
        return get_secret(primary)
    except Exception:
        try:
            return get_secret(fallback)
        except Exception as e:
            raise RuntimeError(f"Secrets '{primary}' and '{fallback}' not found.") from e


def generate_answer(query: str, context_docs: list) -> dict:
    """
    Calls Azure OpenAI Chat Completion to generate a contextual response
    based on retrieved PubMed docs.
    """
    try:
        # 🔐 Fetch secrets (supports both hyphen and underscore styles)
        endpoint = _get_secret_with_fallback("azure-openai-endpoint", "AZURE_OPENAI_ENDPOINT")
        api_key  = _get_secret_with_fallback("azure-openai-key", "AZURE_OPENAI_KEY")

        # 💡 Deployment name (override via env var if needed)
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")

        url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version=2024-05-01-preview"

        # 📚 Combine retrieved docs into context text
        context_text = "\n\n".join(
            [f"[{d.get('pmid', 'N/A')}] {d.get('title', '')}: {d.get('abstract', '')}" for d in context_docs]
        ) or "No relevant context found."

        prompt = (
            f"Answer the following question based on the given PubMed abstracts.\n\n"
            f"Context:\n{context_text}\n\nQuestion:\n{query}\n\nAnswer:"
        )

        headers = {"Content-Type": "application/json", "api-key": api_key}
        payload = {"messages": [{"role": "user", "content": prompt}],
                   "max_tokens": 512, "temperature": 0.3}

        logger.info(f"🧠 Sending generation request to Azure OpenAI for query: '{query}'")

        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        data = response.json()
        answer = data["choices"][0]["message"]["content"].strip()

        logger.info("✅ Successfully generated response from Azure OpenAI.")
        return {"query": query, "answer": answer, "context_used": len(context_docs)}

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ OpenAI API call failed: {e}", exc_info=True)
        return {"query": query, "error": str(e)}
    except Exception as e:
        logger.error(f"⚠️ Generation failed: {e}", exc_info=True)
        return {"query": query, "error": str(e)}


# ---------------------------------------------------------------------------
# CLI Test – python3 -m pubmed_pipeline.rag.rag_generator
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    logger.info("🧩 Running generator self-test.")
    mock_docs = [
        {"pmid": "12345", "title": "Cisplatin and S-1 in gastric cancer",
         "abstract": "Clinical outcomes improved in combination."},
        {"pmid": "67890", "title": "Comparative study of chemotherapy regimens",
         "abstract": "Evaluated efficacy and toxicity."}
    ]
    result = generate_answer("cisplatin S-1 gastric cancer outcomes", mock_docs)
    print(json.dumps(result, indent=2))
    logger.info("🏁 Generator self-test completed.")
    print(f"✅ Log entries written to: {os.path.expanduser('~/pubmed_pipeline/data/logs/rag_pipeline/rag.log')}")
