"""Email Draft Agent implementation for MeetingMind AI.

This module implements the EmailAgent which inherits from BaseAgent.
It automatically loads instructions from the email_writer/SKILL.md file,
initializes the Google ADK Agent, and uses it to draft professional follow-up emails.
"""

import json
import logging
from typing import Optional, Dict, List, Any, Union

from google.adk.sessions import InMemorySessionService
from src.agents.base_agent import BaseAgent

logger = logging.getLogger("meetingmind.agents.email")


class EmailAgent(BaseAgent):
    """Agent responsible for drafting a professional follow-up email."""

    def __init__(
        self,
        name: str = "EmailAgent",
        model_name: str = "gemini-2.5-flash",
        session_service: Optional[InMemorySessionService] = None,
    ) -> None:
        """Initializes the EmailAgent and automatically loads its skill.

        Args:
            name: The name of the agent.
            model_name: The Gemini model name to use.
            session_service: Optional session service for dependency injection.
        """
        super().__init__(name=name, model_name=model_name)
        # Load skill automatically
        self.load_skill("email_writer")
        # Store base instruction template for formatting
        self.base_instruction: str = self.instruction
        # Dependency injection for session service
        self.session_service: InMemorySessionService = session_service or InMemorySessionService()

    def generate_email(
        self,
        summary: Optional[Dict[str, Any]],
        tasks: Optional[List[Dict[str, Any]]],
    ) -> Dict[str, Any]:
        """Generates a professional follow-up email using summary and tasks.

        Args:
            summary: The structured meeting summary dict.
            tasks: The structured tasks list.

        Returns:
            Dict[str, Any]: Structured JSON follow-up email containing 'subject'
                and 'body', or an error response dictionary if validation fails.
        """
        logger.info("Starting email drafting task.")

        # Validate missing inputs
        if summary is None:
            logger.warning("Summary is missing.")
            return {"error": "Summary is missing."}
        if tasks is None:
            logger.warning("Tasks are missing.")
            return {"error": "Tasks are missing."}

        # Validate empty inputs
        if not summary:
            logger.warning("Summary is empty.")
            return {"error": "Summary is empty."}
        if not tasks:
            logger.warning("Task list is empty.")
            return {"error": "Task list is empty."}

        # Format inputs as JSON string and replace placeholders in template
        summary_str = json.dumps(summary, indent=2)
        tasks_str = json.dumps(tasks, indent=2)
        instruction_with_data = self.base_instruction.replace(
            "{summary}", summary_str
        ).replace(
            "{tasks}", tasks_str
        )
        self.instruction = instruction_with_data

        # Reset ADK Agent so it gets re-initialized with updated instruction
        self.adk_agent = None

        return self._execute(prompt="Please generate the email.", session_service=self.session_service)
