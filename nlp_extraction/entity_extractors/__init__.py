"""
entity_extractors/biobert_extractor.py
--------------------------------------
Performs biomedical Named Entity Recognition using BioBERT via Hugging Face Transformers.
Compatible with Python 3.13 (no SpaCy dependency).
"""

from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from typing import List, Dict

# Load pretrained BioBERT model
MODEL_NAME = "d4data/biomedical-ner-all"

print(f"Loading BioBERT model: {MODEL_NAME} ...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME)
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")
print("✅ BioBERT model loaded successfully.")

def extract_entities_biobert(text: str) -> List[Dict]:
    """
    Extract biomedical entities from a given text.
    Returns: list of {text, label, start, end, score}
    """
    if not text.strip():
        return []

    outputs = ner_pipeline(text)
    results = []
    for ent in outputs:
        label = ent["entity_group"].upper()
        if label in {"DRUG", "DISEASE", "CHEMICAL", "GENE", "PROTEIN"}:
            results.append({
                "text": ent["word"].strip(),
                "label": label,
                "start": int(ent["start"]),
                "end": int(ent["end"]),
                "score": round(float(ent["score"]), 3)
            })
    return results
