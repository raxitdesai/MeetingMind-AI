"""Logging configuration for MeetingMind AI.

This module provides setup_logging to configure the logging format and handlers.
"""

import logging
import sys

def setup_logging(level: int = logging.INFO) -> None:
    """Configures the root logger for the application with a clean, structured format.

    Args:
        level: The default logging level to set (e.g. logging.INFO).
    """
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Clean existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    root_logger.addHandler(console_handler)
    root_logger.setLevel(level)

    # Log bootstrap event
    logger = logging.getLogger("meetingmind.logging")
    logger.debug("Structured logging initialized successfully.")
