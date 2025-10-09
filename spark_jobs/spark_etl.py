"""
Layer 3.5 – PySpark ETL over Kafka Stub
Reads JSON files from data/streaming/ (Kafka stub) → performs light transforms → preview + persist.
"""

# ----------------------------------------------------------
# 🩹 Compatibility patch for Python 3.12/3.13 + PySpark
# ----------------------------------------------------------
import sys, types
if "typing" in sys.modules:
    import typing
    # Newer Python versions removed typing.io and typing.re
    if not hasattr(typing, "io"):
        typing.io = types.SimpleNamespace(BinaryIO=bytes, TextIO=str)
    if not hasattr(typing, "re"):
        typing.re = types.SimpleNamespace(Pattern=str, Match=str)
# ----------------------------------------------------------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, trim
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STREAM_DIR = os.path.join(BASE_DIR, "data", "streaming")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "spark_output")

# Start Spark
spark = (
    SparkSession.builder
    .appName("PubMedStubETL")
    .master("local[*]")
    .config("spark.sql.shuffle.partitions", "4")
    .getOrCreate()
)

print(f"🚀 Reading streaming stub files from: {STREAM_DIR}")

# Read all stubbed Kafka JSON files
df = spark.read.json(f"{STREAM_DIR}/*.json")

# Basic sanity check
print(f"Total records: {df.count()}")
df.select("pmid", "title").show(5, truncate=False)

# Simple transformations
clean_df = (
    df.withColumn("pmid", trim(col("pmid")))
      .withColumn("title", trim(lower(col("title"))))
)

# Write to Parquet for later stages
os.makedirs(OUTPUT_DIR, exist_ok=True)
clean_df.write.mode("overwrite").parquet(os.path.join(OUTPUT_DIR, "pubmed_clean.parquet"))

print(f"✅ Spark ETL completed → {OUTPUT_DIR}/pubmed_clean.parquet")
spark.stop()
