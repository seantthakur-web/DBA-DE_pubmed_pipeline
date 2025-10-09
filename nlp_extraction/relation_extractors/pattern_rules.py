"""
relation_extractors/pattern_rules.py
------------------------------------
Lightweight rule-based relationship extractor.

Scans text for biomedical trigger verbs (treats, inhibits, causes)
and builds triples using the entities found by BioBERT.
"""

from typing import List, Dict
import re

# trigger words for relationships
TREAT_TRIGGERS = {"treat", "therapy", "used for", "effective against"}
CAUSE_TRIGGERS = {"cause", "induce", "lead to", "result in", "associated with"}
INHIBIT_TRIGGERS = {"inhibit", "suppress", "block"}

def extract_relations(text: str, entities: List[Dict]) -> List[Dict]:
    """
    Generate rule-based relationships between entities.

    Args:
        text: full abstract or sentence
        entities: list of entity dicts (from BioBERT)
    Returns:
        list of relation dicts: [{subject, predicate, object}]
    """
    lowered = text.lower()
    relations = []

    # group entities by type
    drugs = [e for e in entities if e["label"] in {"CHEMICAL", "DRUG"}]
    diseases = [e for e in entities if e["label"] == "DISEASE"]

    # decide predicate based on trigger words
    predicate = None
    if any(w in lowered for w in TREAT_TRIGGERS):
        predicate = "TREATS"
    elif any(w in lowered for w in INHIBIT_TRIGGERS):
        predicate = "INHIBITS"
    elif any(w in lowered for w in CAUSE_TRIGGERS):
        predicate = "CAUSES"

    # build all pair combinations
    if predicate:
        for d in drugs:
            for dis in diseases:
                relations.append({
                    "subject": d["text"],
                    "predicate": predicate,
                    "object": dis["text"]
                })
    return relations
