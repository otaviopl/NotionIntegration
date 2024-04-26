import os
import logging.config
from dotenv import load_dotenv


def create_logger():
    load_dotenv()
    log_file_path = os.getenv("LOG_PATH")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file_path + "log_file.txt"),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(__name__)
