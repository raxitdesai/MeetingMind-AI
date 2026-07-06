"""Reviewer Agent implementation for MeetingMind AI.

This module implements the ReviewerAgent which inherits from BaseAgent.
It automatically loads instructions from the reviewer/SKILL.md file,
initializes the Google ADK Agent, and uses it to evaluate summaries,
action items, and email drafts.
"""

import json
import logging
from typing import Optional, Dict, List, Any

from google.adk.sessions import InMemorySessionService
from src.agents.base_agent import BaseAgent

logger = logging.getLogger("meetingmind.agents.reviewer")


class ReviewerAgent(BaseAgent):
    """Agent responsible for evaluating outputs produced by other agents."""

    def __init__(
        self,
        name: str = "ReviewerAgent",
        model_name: str = "gemini-2.5-flash",
        session_service: Optional[InMemorySessionService] = None,
    ) -> None:
        """Initializes the ReviewerAgent and automatically loads its skill.

        Args:
            name: The name of the agent.
            model_name: The Gemini model name to use.
            session_service: Optional session service for dependency injection.
        """
        super().__init__(name=name, model_name=model_name)
        # Load skill automatically
        self.load_skill("reviewer")
        # Store base instruction template for formatting
        self.base_instruction: str = self.instruction
        # Dependency injection for session service
        self.session_service: InMemorySessionService = session_service or InMemorySessionService()

    def evaluate(
        self,
        summary: Optional[Dict[str, Any]],
        tasks: Optional[List[Dict[str, Any]]],
        email: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Evaluates the summary, tasks, and email for completeness and quality.

        Args:
            summary: The structured meeting summary dict.
            tasks: The structured tasks list.
            email: The structured email dict.

        Returns:
            Dict[str, Any]: Evaluation report containing quality scores, issues,
                and suggestions, or an error response dictionary if validation fails.
        """
        logger.info("Starting output evaluation task.")

        # Validate missing inputs
        if summary is None:
            logger.warning("Summary is missing.")
            return {"error": "Summary is missing."}
        if tasks is None:
            logger.warning("Tasks are missing.")
            return {"error": "Tasks are missing."}
        if email is None:
            logger.warning("Email is missing.")
            return {"error": "Email is missing."}

        # Validate empty inputs
        if not summary:
            logger.warning("Summary is empty.")
            return {"error": "Summary is empty."}
        if not tasks:
            logger.warning("Tasks are empty.")
            return {"error": "Tasks are empty."}
        if not email:
            logger.warning("Email is empty.")
            return {"error": "Email is empty."}

        # Format inputs as JSON string and replace placeholders in template
        summary_str = json.dumps(summary, indent=2)
        tasks_str = json.dumps(tasks, indent=2)
        email_str = json.dumps(email, indent=2)

        instruction_with_data = self.base_instruction.replace(
            "{summary}", summary_str
        ).replace(
            "{tasks}", tasks_str
        ).replace(
            "{email}", email_str
        )
        self.instruction = instruction_with_data

        # Reset ADK Agent so it gets re-initialized with updated instruction
        self.adk_agent = None

        return self._execute(
            prompt="Please evaluate the supplied outputs.",
            session_service=self.session_service
        )
