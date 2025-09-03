"""Logging configuration."""

import logging
import sys
from pathlib import Path

from app.core.config import settings


def setup_logging():
    """Configure application logging."""
    
    # Create logger
    logger = logging.getLogger("football_betting")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Remove existing handlers
    logger.handlers = []
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    if settings.LOG_FILE:
        log_path = Path(settings.LOG_FILE)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(settings.LOG_FILE)
        file_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    logger.info(f"Logging configured. Level: {settings.LOG_LEVEL}")
    
    return logger