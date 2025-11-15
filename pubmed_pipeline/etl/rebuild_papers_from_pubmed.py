import os
import sqlite3
from typing import List

from xml.etree import ElementTree as ET
from Bio import Entrez

from pubmed_pipeline.utils.log_config import get_logger

logger = get_logger(__name__)

# -------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------

PRIMARY_DB = os.path.expanduser(
    "~/pubmed_pipeline/pubmed_pipeline/data/storage/pubmed_etl.db"
)
SECONDARY_DB = os.path.expanduser(
    "~/pubmed_pipeline/etl_output.db"
)

# Use your email if set, otherwise a placeholder
Entrez.email = os.getenv("NCBI_EMAIL", "you@example.com")


# -------------------------------------------------------------------
# DB HELPERS
# -------------------------------------------------------------------

def get_pmids(db_path: str) -> List[str]:
    if not os.path.exists(db_path):
        logger.error(f"SQLite DB not found: {db_path}")
        return []
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT pmid FROM papers;")
    pmids = [row[0] for row in cur.fetchall()]
    conn.close()
    return pmids


def update_paper_in_db(db_path: str, pmid: str, title: str, abstract: str) -> None:
    if not os.path.exists(db_path):
        logger.warning(f"DB not found, skipping: {db_path}")
        return
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "UPDATE papers SET title = ?, abstract = ? WHERE pmid = ?;",
        (title, abstract, pmid),
    )
    conn.commit()
    conn.close()


# -------------------------------------------------------------------
# PUBMED HELPERS
# -------------------------------------------------------------------

def fetch_pubmed_xml(pmid: str) -> str:
    """Fetch raw PubMed XML for a given PMID."""
    handle = Entrez.efetch(db="pubmed", id=pmid, rettype="xml", retmode="xml")
    xml = handle.read()
    handle.close()
    return xml


def parse_title_and_abstract(xml: str) -> (str, str):
    """
    Parse ArticleTitle and all AbstractText blocks from PubMed XML.
    Concatenate multi-part abstracts into a single string.
    """
    root = ET.fromstring(xml)

    # ArticleTitle
    article = root.find(".//Article")
    if article is None:
        return "", ""

    title_el = article.find("ArticleTitle")
    if title_el is not None:
        title = "".join(title_el.itertext()).strip()
    else:
        title = ""

    # Abstract
    abstract_el = article.find("Abstract")
    if abstract_el is None:
        return title, ""

    parts = []
    for abst in abstract_el.findall("AbstractText"):
        label = abst.get("Label")
        content = "".join(abst.itertext()).strip()
        if not content:
            continue
        if label:
            parts.append(f"{label}: {content}")
        else:
            parts.append(content)

    abstract = "\n\n".join(parts)
    return title, abstract


# -------------------------------------------------------------------
# MAIN REBUILD LOGIC
# -------------------------------------------------------------------

def main():
    logger.info("Starting PubMed papers rebuild from live PubMed XML…")

    pmids = get_pmids(PRIMARY_DB)
    logger.info(f"Found {len(pmids)} PMIDs in PRIMARY_DB.")

    if not pmids:
        logger.error("No PMIDs found. Aborting.")
        return

    for idx, pmid in enumerate(pmids, start=1):
        try:
            logger.info(f"[{idx}/{len(pmids)}] Fetching PMID={pmid}…")
            xml = fetch_pubmed_xml(pmid)
            title, abstract = parse_title_and_abstract(xml)

            if not title and not abstract:
                logger.warning(f"PMID={pmid} has no title/abstract in PubMed XML.")
                continue

            # Update both DBs to keep them consistent
            update_paper_in_db(PRIMARY_DB, pmid, title, abstract)
            update_paper_in_db(SECONDARY_DB, pmid, title, abstract)

        except Exception as e:
            logger.exception(f"Failed to rebuild paper for PMID={pmid}: {e}")

    logger.info("Rebuild complete. Titles and abstracts refreshed from PubMed.")


if __name__ == "__main__":
    main()
