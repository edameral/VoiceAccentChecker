import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
from ..config.settings import settings


def setup_logger():
    """Configure application logging"""
    logger = logging.getLogger("pronunciation_assessment")
    logger.setLevel(settings.log_level.upper())

    # Create logs directory if it doesn't exist
    settings.log_file.parent.mkdir(exist_ok=True)

    # File handler with rotation
    file_handler = RotatingFileHandler(
        settings.log_file,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(levelname)s - %(message)s'
    ))

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger()