import logging
from pathlib import Path


def setup_logger() -> logging.Logger:
    Path("logs").mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler("logs/jarvis.log"),
            logging.StreamHandler(),
        ],
    )

    return logging.getLogger("jarvis")