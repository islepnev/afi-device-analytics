import logging
import os
from dotenv import load_dotenv

def setup_logging():
    """
    Set up logging using the log level from environment variables.
    Default log level is INFO.
    """
    load_dotenv()
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
