"""Main entry point for MeetingMind AI skeleton.

Initializes logging, loads config, and demonstrates successful system bootstrap.
"""

import sys
import logging
from config import validate_config

# Configure application logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("meetingmind.main")

def main() -> None:
    """Bootstraps the application skeleton and validates settings."""
    logger.info("Initializing MeetingMind AI Skeleton...")
    
    if not validate_config():
        logger.error("Configuration validation failed. Exiting.")
        sys.exit(1)
        
    logger.info("MeetingMind AI Skeleton successfully initialized and validated.")

if __name__ == "__main__":
    main()
