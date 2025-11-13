# ============================================================
# 🧪 Unit + Functional Tests for rag_generator.py (INNVO-492)
# ------------------------------------------------------------
# Validates Key Vault secret loading, generation behavior,
# fallback handling, and unified logging.
# Run with: python3 -m pytest -v pubmed_pipeline/tests/test_rag_generator.py
# ============================================================

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import pytest
from unittest.mock import patch, MagicMock
from pubmed_pipeline.rag import rag_generator

# ------------------------------------------------------------
# 🔧 Fixtures
# ------------------------------------------------------------
@pytest.fixture
def sample_docs():
    return [
        {"title": "Cisplatin and S-1 improve survival in gastric cancer",
         "abstract": "Study comparing outcomes in gastric adenocarcinoma patients."},
        {"title": "Fluorouracil-based regimens in gastric carcinoma",
         "abstract": "Meta-analysis showing improved response rates with fluorouracil combinations."}
    ]

# ------------------------------------------------------------
# ✅ Test 1: Secure KeyVault secret loading
# ------------------------------------------------------------
@patch("pubmed_pipeline.rag.rag_generator.get_secret")
def test_keyvault_secret_loading(mock_get_secret):
    mock_get_secret.side_effect = lambda key: f"mock_{key.lower()}"
    from importlib import reload
    reload(rag_generator)
    assert "mock_azure_openai_key" in rag_generator.AZURE_OPENAI_KEY.lower()

# ------------------------------------------------------------
# ✅ Test 2: Generation returns structured JSON
# ------------------------------------------------------------
@patch("pubmed_pipeline.rag.rag_generator.client")
def test_generate_answer_returns_json(mock_client, sample_docs):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Mock summary output"))]
    mock_client.chat.completions.create.return_value = mock_response

    result = rag_generator.generate_answer("cisplatin S-1 gastric cancer outcomes", sample_docs)
    assert isinstance(result, dict)
    assert "answer" in result
    assert len(result["sources"]) == 2

# ------------------------------------------------------------
# ✅ Test 3: Handles empty retrieved_docs gracefully
# ------------------------------------------------------------
def test_generate_answer_with_no_docs():
    result = rag_generator.generate_answer("gastric cancer", [])
    assert result["answer"].startswith("Insufficient context")
    assert result["num_docs"] == 0

# ------------------------------------------------------------
# ✅ Test 4: Logs contain expected entries
# ------------------------------------------------------------
def test_logging_output(sample_docs, caplog):
    with patch("pubmed_pipeline.rag.rag_generator.client.chat.completions.create") as mock_gen:
        mock_gen.return_value.choices = [MagicMock(message=MagicMock(content="Log test summary"))]
        _ = rag_generator.generate_answer("cisplatin S-1 gastric cancer outcomes", sample_docs)

    log_messages = [r.message for r in caplog.records]
    assert any("🧠 Generating summary" in msg for msg in log_messages)
