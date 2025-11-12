#!/usr/bin/env python3
import time
import sys, os
sys.path.append(os.path.expanduser("~/DBA-DE_pubmed_pipeline"))
from utils.log_config import get_logger

logger = get_logger("spark_producer")

def main():
    """
    Simulates Spark-based PubMed ETL and sends messages to Service Bus.
    """
    logger.info("🚀 Starting Spark Producer simulation...")

    try:
        for i in range(3):
            record = f"📄 Mock PubMed record #{i + 1}"
            logger.info(f"📤 Produced message: {record}")
            time.sleep(1)

        logger.info("✅ Spark Producer completed successfully.")
    except Exception as e:
        logger.error(f"❌ Spark Producer failed: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()

