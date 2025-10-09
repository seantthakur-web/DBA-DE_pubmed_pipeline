# etl/verify_etl.py
import sqlite3

db_path = "data/storage/pubmed_etl.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# --- Papers ---
print("=== Papers ===")
for row in cur.execute("SELECT pmid, title FROM papers LIMIT 5;"):
    print(row)

# --- Entities ---
print("\n=== Entities ===")
for row in cur.execute("SELECT name, type FROM entities LIMIT 10;"):
    print(row)

# --- Relations ---
print("\n=== Relations ===")
for row in cur.execute("SELECT subject_id, predicate, object_id FROM relations LIMIT 10;"):
    print(row)

conn.close()
