"""
BioBERT inference module — wraps model loading and prediction.
"""
# TODO: integrate with your existing BioBERT setup (nlp_extractor.py)

class BioBERTModel:
    def __init__(self):
        print("🔄 Loading BioBERT model... (stub)")
        # Load real model here

    def extract_entities(self, text: str):
        """Return dummy entities until integrated."""
        return [{"entity": "GENE", "value": "TP53"}]
