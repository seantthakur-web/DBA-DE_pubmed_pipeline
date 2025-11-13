# etl/schema_definitions.py
def create_tables(conn):
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS papers (
        pmid TEXT PRIMARY KEY,
        title TEXT,
        abstract TEXT
    );

    CREATE TABLE IF NOT EXISTS entities (
        entity_id TEXT PRIMARY KEY,
        name TEXT,
        type TEXT
    );

    CREATE TABLE IF NOT EXISTS relations (
        relation_id TEXT PRIMARY KEY,
        subject_id TEXT,
        predicate TEXT,
        object_id TEXT,
        FOREIGN KEY(subject_id) REFERENCES entities(entity_id),
        FOREIGN KEY(object_id) REFERENCES entities(entity_id)
    );
    """)
# etl/schema_definitions.py
def create_tables(conn):
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS papers (
        pmid TEXT PRIMARY KEY,
        title TEXT,
        abstract TEXT
    );

    CREATE TABLE IF NOT EXISTS entities (
        entity_id TEXT PRIMARY KEY,
        name TEXT,
        type TEXT
    );

    CREATE TABLE IF NOT EXISTS relations (
        relation_id TEXT PRIMARY KEY,
        subject_id TEXT,
        predicate TEXT,
        object_id TEXT,
        FOREIGN KEY(subject_id) REFERENCES entities(entity_id),
        FOREIGN KEY(object_id) REFERENCES entities(entity_id)
    );
    """)
