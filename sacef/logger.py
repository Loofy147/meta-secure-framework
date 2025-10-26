import logging
import sys

def setup_logging(log_file=None, log_level_str='INFO'):
    """
    Configures a structured logger for the framework.
    """
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)

    # Use a specific, named logger to avoid interfering with other libraries
    logger = logging.getLogger('sacef')
    logger.setLevel(log_level)

    # Prevent duplicate handlers if this function is called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create a formatter for structured logging
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # If a log file is provided, add a file handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Always add a console handler to print to stdout
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger
