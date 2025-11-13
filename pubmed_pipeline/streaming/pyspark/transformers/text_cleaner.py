"""
Utility functions for text cleaning and normalization.
"""
import re

def clean_text(text: str) -> str:
    """Basic cleaner for PubMed abstracts."""
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text
