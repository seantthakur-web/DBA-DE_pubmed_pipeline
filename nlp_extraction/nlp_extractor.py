"""
Layer 2 – NLP Extraction
Extracts biomedical named entities from raw PubMed JSONs using BioBERT.
"""

import os
import json
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline


# ------------------------------------------------------------
# 🧠 Step 1: Load BioBERT model
# ------------------------------------------------------------
print("Loading BioBERT model: d4data/biomedical-ner-all ...")
tokenizer = AutoTokenizer.from_pretrained("d4data/biomedical-ner-all")
model = AutoModelForTokenClassification.from_pretrained("d4data/biomedical-ner-all")
nlp_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")
print("✅ BioBERT model loaded successfully.\n")


# ------------------------------------------------------------
# 🔧 Extract title + abstract text from PubMed JSON
# ------------------------------------------------------------
def extract_pubmed_text(pubmed_json):
    """
    Extracts title + abstract text from the simplified PubMed JSON format
    where top-level key is 'MedlineCitation'.
    """
    try:
        article = pubmed_json["MedlineCitation"]["Article"]

        title = article.get("ArticleTitle", "")
        abstract_obj = article.get("Abstract", {})

        if isinstance(abstract_obj, dict):
            abstract_text = " ".join(abstract_obj.get("AbstractText", []))
        elif isinstance(abstract_obj, list):
            abstract_text = " ".join(abstract_obj)
        else:
            abstract_text = str(abstract_obj)

        text = f"{title}. {abstract_text}"
        return text.strip()
    except Exception:
        return ""


# ------------------------------------------------------------
# 🧩 Extract entities from text using BioBERT
# ------------------------------------------------------------
def extract_entities_from_text(text):
    """Run BioBERT NER pipeline and format entities."""
    if not text.strip():
        return []

    try:
        entities = nlp_pipeline(text)
        formatted = [
            {"text": ent["word"], "label": ent["entity_group"], "score": float(ent["score"])}
            for ent in entities
        ]
        return formatted
    except Exception as e:
        print(f"⚠️  Extraction error: {e}")
        return []


# ------------------------------------------------------------
# 🚀 Main NLP extraction loop
# ------------------------------------------------------------
def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    raw_dir = os.path.join(base_dir, "data", "raw")
    extracted_dir = os.path.join(base_dir, "data", "extracted")
    os.makedirs(extracted_dir, exist_ok=True)

    output_path = os.path.join(
        extracted_dir, f"nlp_extracted_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    )

    extracted_data = []
    total_files = len([f for f in os.listdir(raw_dir) if f.endswith(".json")])
    processed = 0
    skipped = 0

    for filename in os.listdir(raw_dir):
        if not filename.endswith(".json"):
            continue

        file_path = os.path.join(raw_dir, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception:
                print(f"⚠️  Skipping invalid JSON: {filename}")
                skipped += 1
                continue

        text = extract_pubmed_text(data)
        if not text:
            print(f"⚠️  No abstract/text found in {filename}")
            skipped += 1
            continue

        print(f"🔍 ({processed+1}/{total_files}) Processing: {filename}")
        entities = extract_entities_from_text(text)

        extracted_data.append({
            "pmid": os.path.splitext(filename)[0],
            "title": text[:100],  # short preview
            "entities": entities,
            "relations": []  # placeholder for relation extraction
        })

        processed += 1

    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(extracted_data, out, indent=2)

    print(f"\n💾 Saved extracted data to: {output_path}")
    print(f"✅ Completed. {processed} processed, {skipped} skipped.")


if __name__ == "__main__":
    main()
