from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, trim
import os

# Initialize Spark
spark = SparkSession.builder \
    .appName("PubMed_ETL_Analysis") \
    .config("spark.driver.extraJavaOptions", "-Dfile.encoding=utf-8") \
    .getOrCreate()

# Paths
db_path = "etl_output.db"
output_dir = "data/processed"
os.makedirs(output_dir, exist_ok=True)

print("🚀 Starting PySpark analysis...")

# Load tables from SQLite
papers_df = spark.read.format("jdbc") \
    .option("url", f"jdbc:sqlite:{db_path}") \
    .option("dbtable", "papers") \
    .load()

entities_df = spark.read.format("jdbc") \
    .option("url", f"jdbc:sqlite:{db_path}") \
    .option("dbtable", "entities") \
    .load()

print(f"📚 Loaded {papers_df.count()} papers and {entities_df.count()} entities")

# Clean entities
entities_clean = (
    entities_df
    .withColumn("text", trim(lower(col("text"))))
    .filter(col("text").isNotNull())
)

# Simple aggregation: entity counts by label
agg_df = entities_clean.groupBy("label").count().orderBy(col("count").desc())
agg_df.show(10, truncate=False)

# Save outputs
entities_clean.write.mode("overwrite").parquet(os.path.join(output_dir, "entities_clean.parquet"))
agg_df.write.mode("overwrite").parquet(os.path.join(output_dir, "entity_summary.parquet"))

print("✅ PySpark ETL complete → data/processed/")
spark.stop()
