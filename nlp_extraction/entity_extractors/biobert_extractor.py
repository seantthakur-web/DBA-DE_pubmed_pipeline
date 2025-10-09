from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from typing import List, Dict
import re

MODEL_NAME = "d4data/biomedical-ner-all"

print(f"🔄 Loading BioBERT model: {MODEL_NAME} ...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME)
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple", device=-1)
print("✅ BioBERT model loaded successfully.\n")

# simple biomedical keyword lists for fallback
DRUG_HINTS = {"fluorouracil", "cisplatin", "oxaliplatin", "paclitaxel", "s-1"}
DISEASE_HINTS = {"gastric", "carcinoma", "colorectal", "adenocarcinoma", "cancer"}

def extract_entities_biobert(text: str) -> List[Dict]:
    """Run BioBERT NER and apply rule-based fallback."""
    text = text.strip()
    if not text:
        return []

    # 1️⃣ model predictions
    outputs = ner_pipeline(text)
    results = [
        {
            "text": ent["word"].strip(),
            "label": ent["entity_group"].upper(),
            "start": int(ent["start"]),
            "end": int(ent["end"]),
            "score": round(float(ent["score"]), 3)
        }
        for ent in outputs
        if ent["entity_group"].upper() in {"DRUG", "DISEASE", "CHEMICAL", "GENE", "PROTEIN"}
    ]

    # 2️⃣ fallback pattern detection
    lowered = text.lower()
    for w in DRUG_HINTS:
        if re.search(rf"\b{re.escape(w)}\b", lowered):
            results.append({"text": w, "label": "CHEMICAL", "start": lowered.find(w), "end": lowered.find(w)+len(w), "score": 0.8})
    for w in DISEASE_HINTS:
        if re.search(rf"\b{re.escape(w)}\b", lowered):
            span = lowered.find(w)
            results.append({"text": w, "label": "DISEASE", "start": span, "end": span+len(w), "score": 0.7})

    # 3️⃣ deduplicate
    seen = set()
    unique = []
    for e in results:
        key = (e["text"].lower(), e["label"])
        if key not in seen:
            seen.add(key)
            unique.append(e)
    return unique
