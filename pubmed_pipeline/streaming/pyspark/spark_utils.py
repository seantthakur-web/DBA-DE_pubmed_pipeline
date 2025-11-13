"""
Spark utilities for session creation and schema definitions.
"""
from pyspark.sql import SparkSession

def get_spark(app_name="PubMedStreamingApp"):
    """Return a configured SparkSession."""
    spark = (
        SparkSession.builder
        .appName(app_name)
        .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true")
        .config("spark.sql.shuffle.partitions", "2")
        .getOrCreate()
    )
    return spark
