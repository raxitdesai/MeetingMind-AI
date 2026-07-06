"""Main entry point for MeetingMind AI.

Initializes logging, configuration, and bootstraps the ADK application foundation.
"""

import sys
import logging
from src.config import validate_config
from src.core.logging_config import setup_logging
from src.core.app import MeetingMindApp

# Configure application logging using the core structured logging configuration
setup_logging(level=logging.INFO)
logger = logging.getLogger("meetingmind.main")

def main() -> None:
    """Bootstraps the application and validates configuration settings."""
    logger.info("Initializing MeetingMind AI Foundation...")

    if not validate_config():
        logger.error("Configuration validation failed. Exiting.")
        sys.exit(1)

    try:
        # Initialize and bootstrap the application wrapper
        app = MeetingMindApp()
        app.bootstrap()
        logger.info("MeetingMind AI ADK Foundation successfully bootstrapped.")
    except Exception as e:
        logger.critical("Failed to bootstrap the application: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
