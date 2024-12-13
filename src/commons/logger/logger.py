import logging
from logging.handlers import RotatingFileHandler


# configure logging
LOG_FILE = "app.log"


def setup_logger():
    # root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # formatter for all handlers
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
