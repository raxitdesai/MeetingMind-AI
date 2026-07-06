"""Base agent foundation for MeetingMind AI.

This module provides the BaseAgent class, wrapping the Google ADK Agent,
and including utility methods to load prompt instructions from skill definitions.
"""

import logging
from typing import Optional
from google.adk import Agent
from config import BASE_DIR

logger = logging.getLogger("meetingmind.agents.base")

class BaseAgent:
    """Base class for all MeetingMind AI agents wrapping the Google ADK Agent."""

    def __init__(
        self,
        name: str,
        model_name: str = "gemini-2.5-flash",
        instruction: str = ""
    ) -> None:
        """Initializes the base agent.

        Args:
            name: The name of the agent.
            model_name: The Gemini model name to use.
            instruction: Default instruction or prompt for the agent.
        """
        self.name: str = name
        self.model_name: str = model_name
        self.instruction: str = instruction
        self.adk_agent: Optional[Agent] = None

    def load_skill(self, skill_folder: str) -> None:
        """Loads prompt and instructions from the corresponding SKILL.md file.

        Args:
            skill_folder: The folder name under .agent/skills/ containing SKILL.md.

        Raises:
            FileNotFoundError: If the SKILL.md file does not exist.
        """
        skill_path = BASE_DIR / ".agent" / "skills" / skill_folder / "SKILL.md"
        if not skill_path.exists():
            logger.error("Skill file not found at %s", skill_path)
            raise FileNotFoundError(f"Skill file not found at {skill_path}")

        try:
            with open(skill_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse frontmatter (delimited by ---) and keep the body as prompt instructions
            parts = content.split("---", 2)
            if len(parts) >= 3:
                body = parts[2].strip()
                self.instruction = body
                logger.info(
                    "Successfully loaded instructions for agent '%s' from skill '%s'",
                    self.name,
                    skill_folder
                )
            else:
                self.instruction = content.strip()
                logger.warning(
                    "Could not parse frontmatter in %s. Loaded entire file as instruction.",
                    skill_path
                )

        except Exception as e:
            logger.error("Error reading skill file %s: %s", skill_path, e)
            raise

    def initialize_adk_agent(self) -> None:
        """Initializes the underlying Google ADK Agent instance."""
        logger.info("Initializing ADK Agent '%s' with model '%s'...", self.name, self.model_name)
        self.adk_agent = Agent(
            name=self.name,
            model=self.model_name,
            instruction=self.instruction
        )
        logger.info("ADK Agent '%s' initialized successfully.", self.name)
