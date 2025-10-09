"""
Main PySpark Structured Streaming job:
Reads PubMed messages from Kafka and processes them with BioBERT.
"""
from streaming.pyspark.spark_utils import get_spark
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType
import json

def main():
    spark = get_spark("PubMedNLPConsumer")

    schema = StructType().add("pmid", StringType()).add("xml", StringType())

    df = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "localhost:9092")
        .option("subscribe", "pubmed_raw")
        .load()
    )

    parsed = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

    def process_row(row):
        print(f"🧠 Processing PMID {row.pmid}")
        # TODO: Call BioBERT here

    query = parsed.writeStream.foreach(process_row).start()
    query.awaitTermination()

if __name__ == "__main__":
    main()
