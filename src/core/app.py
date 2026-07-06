"""Core application bootstrap for MeetingMind AI.

This module initializes the application configurations, sets up logging,
configures the Gemini client, and holds the AgentRegistry.
"""

import logging
from typing import Optional
from google import genai
from core.registry import AgentRegistry
from config import GEMINI_API_KEY, validate_config

logger = logging.getLogger("meetingmind.app")

class MeetingMindApp:
    """Bootstraps and manages the application lifecycle and dependencies."""

    def __init__(self, registry: Optional[AgentRegistry] = None) -> None:
        """Initializes the application instance.

        Args:
            registry: Optional AgentRegistry instance. If not provided, a new one is created.
        """
        self.registry: AgentRegistry = registry or AgentRegistry()
        self.genai_client: Optional[genai.Client] = None
        self._is_initialized: bool = False

    def bootstrap(self) -> None:
        """Bootstraps the application by loading configuration and initializing clients.

        Raises:
            RuntimeError: If configuration validation fails.
        """
        logger.info("Bootstrapping MeetingMind AI ADK Application...")

        # Validate configuration
        if not validate_config():
            raise RuntimeError("Configuration validation failed. Cannot bootstrap application.")

        # Initialize the Google GenAI client
        # By using the standard google-genai client, we prepare the API interface for agents.
        try:
            logger.info("Initializing Google GenAI Client...")
            self.genai_client = genai.Client(api_key=GEMINI_API_KEY)
            logger.info("Google GenAI Client successfully initialized.")
        except Exception as e:
            logger.error("Failed to initialize Google GenAI Client: %s", e)
            raise RuntimeError(f"GenAI Client initialization failed: {e}") from e

        self._is_initialized = True
        logger.info("Application bootstrap completed successfully.")

    @property
    def is_initialized(self) -> bool:
        """Checks if the application has been successfully initialized.

        Returns:
            bool: True if initialized, False otherwise.
        """
        return self._is_initialized
