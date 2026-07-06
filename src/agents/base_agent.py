"""Base agent foundation for MeetingMind AI.

This module provides the BaseAgent class, wrapping the Google ADK Agent,
and including utility methods to load prompt instructions from skill definitions.
"""

import asyncio
import json
import logging
from typing import Optional, Dict, Any
from google.adk import Agent, Runner
from google.adk.sessions import InMemorySessionService
from src.config import BASE_DIR

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

    def _execute(
        self,
        prompt: str,
        session_service: Optional[InMemorySessionService] = None
    ) -> Dict[str, Any]:
        """Executes the agent task using Google ADK and processes the response.

        Args:
            prompt: The prompt to run.
            session_service: Optional session service.

        Returns:
            Dict[str, Any]: Parsed JSON response or error dictionary.
        """
        logger.info("Executing agent task with prompt: %s", prompt)
        try:
            if self.adk_agent is None:
                self.initialize_adk_agent()

            s_service = session_service or getattr(self, "session_service", None) or InMemorySessionService()

            runner = Runner(
                agent=self.adk_agent,
                app_name="meetingmind_app",
                session_service=s_service
            )

            # Invoke the agent asynchronously and wait for the results
            logger.info("Invoking Gemini via ADK runner...")
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            if loop.is_running():
                events = loop.run_until_complete(runner.run_debug(prompt))
            else:
                events = asyncio.run(runner.run_debug(prompt))

            logger.info("Successfully received response events from Gemini.")

            # Extract final response content
            response_text = "".join([
                part.text
                for event in events
                if event.content and event.content.parts
                for part in event.content.parts
                if part.text
            ]).strip()

            if not response_text:
                logger.error("Empty response received from ADK runner.")
                return {"error": "Transcript could not be processed."}

            # Remove markdown code block formatting if returned by model
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            elif response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()

            # Parse JSON
            data: Dict[str, Any] = json.loads(response_text)
            logger.info("Successfully parsed JSON response.")
            return data

        except json.JSONDecodeError as je:
            logger.error("Failed to parse response as JSON: %s. Response content: %s", je, response_text)
            return {"error": "Transcript could not be processed."}
        except Exception as e:
            logger.error("Error occurred during agent execution: %s", e, exc_info=True)
            return {"error": "Transcript could not be processed."}
