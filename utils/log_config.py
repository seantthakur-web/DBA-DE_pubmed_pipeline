import logging
import os
from pathlib import Path

def get_logger(name="pubmed_pipeline"):
    """
    Initializes and returns a logger that writes both to console and
    a persistent log file under ~/DBA-DE_pubmed_pipeline/logs/.
    """
    # Determine project root (two levels above utils/)
    project_root = Path(__file__).resolve().parents[1]
    log_dir = project_root / "logs"
    log_dir.mkdir(exist_ok=True)

    # Log file path
    log_file = log_dir / "pubmed_pipeline.log"

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger(name)
    logger.info("✅ Logger initialized successfully.")
    return logger


# Standalone test
if __name__ == "__main__":
    logger = get_logger()
    logger.info("🧪 Test log message from centralized logger.")
