import time
from utils.log_config import get_logger

logger = get_logger("vector_loader")

def load_to_vector_store():
    logger.info("🚀 Starting Vector Loader simulation...")
    for i in range(1, 4):
        logger.info(f"📥 Consumed message: PubMed vector #{i}")
        time.sleep(1)
    logger.info("✅ Vector Loader completed successfully.")

if __name__ == "__main__":
    load_to_vector_store()

