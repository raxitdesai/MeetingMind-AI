"""Configuration loader for MeetingMind AI.

Responsible for loading environment variables and validating essential settings.
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Setup initial logging
logger = logging.getLogger("meetingmind.config")

# Determine base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    logger.info("Loaded environment variables from %s", env_path)
else:
    logger.warning(".env file not found at %s. Relying on system environment variables.", env_path)

# Configuration values
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def validate_config() -> bool:
    """Validates that all required configuration variables are set.

    Returns:
        bool: True if configuration is valid, False otherwise.
    """
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY is not set in the environment or .env file.")
        return False
    logger.info("Configuration loaded and validated successfully.")
    return True
