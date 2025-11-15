"""
fetch_pubmed_by_query.py

Fetch PubMed articles by keyword queries and store them in the PRIMARY_DB
(SQLite: pubmed_pipeline/data/storage/pubmed_etl.db, table: papers).

Usage:
    python -m pubmed_pipeline.etl.fetch_pubmed_by_query
"""

import os
import time
import sqlite3
from pathlib import Path
from typing import Dict, List, Set, Tuple

from Bio import Entrez

from pubmed_pipeline.utils.log_config import get_logger

logger = get_logger(__name__)

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

# Root of the git repo (~/pubmed_pipeline)
REPO_ROOT = Path(__file__).resolve().parents[2]

# PRIMARY_DB used everywhere else
DB_PATH = REPO_ROOT / "pubmed_pipeline" / "data" / "storage" / "pubmed_etl.db"

# How many results to pull per query
RETMAX = 50

# Respect NCBI usage policy – small pause between calls (in seconds)
NCBI_SLEEP = 0.4

# Replace or merge strategy:
#   True  → wipe papers table before inserting (fresh rebuild)
#   False → upsert into existing rows
FULL_REBUILD = True

# Core domain queries – this is the “shape” of your dataset
QUERIES: List[Dict[str, str]] = [
    {
        "label": "cisplatin_gastric",
        "term": 'cisplatin AND "gastric cancer"[Title/Abstract]',
    },
    {
        "label": "fluorouracil_gastric",
        "term": 'fluorouracil AND "gastric cancer"[Title/Abstract]',
    },
    {
        "label": "S1_gastric",
        "term": '"S-1" AND "gastric cancer"[Title/Abstract]',
    },
    {
        "label": "gastroesophageal_chemo",
        "term": '"gastroesophageal" AND (chemotherapy OR cisplatin OR fluorouracil)',
    },
    {
        "label": "nutrition_gastric",
        "term": '"nutritional support" AND "gastric cancer"[Title/Abstract]',
    },
]


# -------------------------------------------------------------------
# Helpers – Entrez configuration
# -------------------------------------------------------------------

def init_entrez() -> None:
    """
    Initialize Entrez with email (required) and optional API key.
    """
    email = (
        os.getenv("NCBI_EMAIL")
        or os.getenv("ENTREZ_EMAIL")
        or "you@example.com"
    )
    api_key = os.getenv("NCBI_API_KEY") or os.getenv("ENTREZ_API_KEY")

    Entrez.email = email
    if api_key:
        Entrez.api_key = api_key

    logger.info(f"Entrez configured with email={email}, api_key={'SET' if api_key else 'NOT SET'}")


# -------------------------------------------------------------------
# Helpers – SQLite
# -------------------------------------------------------------------

def get_sqlite_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn


def init_papers_table(conn: sqlite3.Connection) -> None:
    """
    Ensure 'papers' table exists with (pmid, title, abstract).
    """
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS papers (
            pmid TEXT PRIMARY KEY,
            title TEXT,
            abstract TEXT
        );
        """
    )
    conn.commit()


def clear_papers(conn: sqlite3.Connection) -> None:
    logger.info("FULL_REBUILD=True → clearing existing rows from papers…")
    conn.execute("DELETE FROM papers;")
    conn.commit()


def insert_paper(conn: sqlite3.Connection, pmid: str, title: str, abstract: str) -> None:
    conn.execute(
        """
        INSERT OR REPLACE INTO papers (pmid, title, abstract)
        VALUES (?, ?, ?);
        """,
        (pmid, title, abstract),
    )


# -------------------------------------------------------------------
# PubMed search + fetch
# -------------------------------------------------------------------

def search_pmids(term: str, retmax: int = RETMAX) -> List[str]:
    """
    Run an Entrez search for a given term and return PMIDs.
    """
    logger.info(f"Searching PubMed for term={term!r}, retmax={retmax}…")
    handle = Entrez.esearch(db="pubmed", term=term, retmax=retmax)
    result = Entrez.read(handle)
    handle.close()
    pmids = result.get("IdList", [])
    logger.info(f"  → Found {len(pmids)} PMIDs")
    time.sleep(NCBI_SLEEP)
    return pmids


def fetch_article(pmid: str) -> Tuple[str, str]:
    """
    Fetch a single PMID as XML, parse title + abstract.
    Returns (title, abstract). Abstract can be empty string.
    """
    logger.debug(f"Fetching PMID={pmid}…")
    handle = Entrez.efetch(db="pubmed", id=pmid, rettype="xml", retmode="xml")
    records = Entrez.read(handle)
    handle.close()
    time.sleep(NCBI_SLEEP)

    if not records or "PubmedArticle" not in records or not records["PubmedArticle"]:
        logger.warning(f"No PubmedArticle found for PMID={pmid}")
        return "", ""

    article = records["PubmedArticle"][0]["MedlineCitation"]["Article"]

    # Title
    title = article.get("ArticleTitle", "")
    # Some titles come as bytes-like / complex objects; ensure string
    if not isinstance(title, str):
        title = str(title)

    # Abstract – join all AbstractText pieces with paragraph breaks
    abstract = ""
    if "Abstract" in article and "AbstractText" in article["Abstract"]:
        parts = article["Abstract"]["AbstractText"]
        # parts can be list of strings or list of dict-like
        texts = []
        for p in parts:
            if isinstance(p, str):
                texts.append(p)
            else:
                texts.append(str(p))
        abstract = "\n\n".join(texts)

    return title.strip(), abstract.strip()


# -------------------------------------------------------------------
# Main pipeline
# -------------------------------------------------------------------

def collect_pmids() -> Dict[str, Set[str]]:
    """
    Run all configured QUERIES and collect PMIDs per label and globally.
    Returns:
        {
            "global": {pmid1, pmid2, ...},
            "label:cisplatin_gastric": {...},
            ...
        }
    """
    pmid_map: Dict[str, Set[str]] = {"global": set()}

    for q in QUERIES:
        label = q["label"]
        term = q["term"]
        pmids = search_pmids(term)
        pmid_set = set(pmids)
        pmid_map[f"label:{label}"] = pmid_set
        pmid_map["global"].update(pmid_set)

    logger.info("=== PMID collection summary ===")
    logger.info(f"Total unique PMIDs: {len(pmid_map['global'])}")
    for q in QUERIES:
        label_key = f"label:{q['label']}"
        logger.info(f"  {label_key}: {len(pmid_map[label_key])} PMIDs")
    logger.info("================================")

    return pmid_map


def rebuild_papers_from_queries() -> None:
    """
    Main orchestrator:
      1. Collect PMIDs from QUERIES
      2. Fetch each PMID’s title + abstract
      3. Store into PRIMARY_DB (papers table)
    """
    init_entrez()
    pmid_map = collect_pmids()
    all_pmids = sorted(pmid_map["global"])

    if not all_pmids:
        logger.warning("No PMIDs collected from queries. Nothing to ingest.")
        return

    conn = get_sqlite_connection()
    try:
        init_papers_table(conn)
        if FULL_REBUILD:
            clear_papers(conn)

        logger.info(f"Beginning fetch + insert for {len(all_pmids)} PMIDs…")

        inserted = 0
        skipped_no_abstract = 0

        for idx, pmid in enumerate(all_pmids, start=1):
            logger.info(f"[{idx}/{len(all_pmids)}] PMID={pmid}")
            try:
                title, abstract = fetch_article(pmid)
            except Exception as e:
                logger.exception(f"Error fetching PMID={pmid}: {e}")
                continue

            if not title and not abstract:
                logger.warning(f"PMID={pmid} has empty title and abstract – skipping.")
                continue

            if not abstract:
                logger.warning(f"PMID={pmid} has no abstract – skipping insert.")
                skipped_no_abstract += 1
                continue

            insert_paper(conn, pmid, title, abstract)
            inserted += 1

            if inserted % 10 == 0:
                conn.commit()

        conn.commit()
        logger.info("=== Rebuild complete ===")
        logger.info(f"Inserted papers with abstracts: {inserted}")
        logger.info(f"Skipped (no abstract): {skipped_no_abstract}")
    finally:
        conn.close()


def main() -> None:
    logger.info("Starting PubMed fetch-from-query rebuild…")
    rebuild_papers_from_queries()
    logger.info("PubMed fetch-from-query rebuild finished.")


if __name__ == "__main__":
    main()
