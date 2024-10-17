# logger.py
import logging
from config.settings import Config

def setup_logger(name):
    """
    Set up a logger with the specified name, level, and log file.
    """
    logger = logging.getLogger(name)
    logger.setLevel(Config.LOG_LEVEL)

    # File handler to write log messages to a file
    file_handler = logging.FileHandler(Config.LOG_FILE)
    file_handler.setLevel(Config.LOG_LEVEL)

    # Console handler to also print log messages to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(Config.LOG_LEVEL)

    # Set up a standard logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Usage Example
logger = setup_logger(__name__)

if __name__ == "__main__":
    logger.info("This is an informational message.")
    logger.error("This is an error message.")
