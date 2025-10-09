# etl/db_utils.py
import sqlite3

def connect_db(db_path):
    """Connect to SQLite database."""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def insert_paper(conn, paper):
    conn.execute("""
        INSERT OR IGNORE INTO papers (pmid, title, abstract)
        VALUES (?, ?, ?)
    """, (paper["pmid"], paper["title"], paper["abstract"]))


def insert_entities(conn, entities):
    conn.executemany("""
        INSERT OR IGNORE INTO entities (entity_id, name, type)
        VALUES (:entity_id, :name, :type)
    """, entities)


def insert_relations(conn, relations):
    conn.executemany("""
        INSERT OR IGNORE INTO relations (relation_id, subject_id, predicate, object_id)
        VALUES (:relation_id, :subject_id, :predicate, :object_id)
    """, relations)
