"""Task Extraction Agent implementation for MeetingMind AI.

This module implements the TaskAgent which inherits from BaseAgent.
It automatically loads instructions from the extract_tasks/SKILL.md file,
initializes the Google ADK Agent, and uses it to extract action items.
"""

import logging
from typing import Optional, Dict, List, Any, Union

from google.adk.sessions import InMemorySessionService
from src.agents.base_agent import BaseAgent

logger = logging.getLogger("meetingmind.agents.task")


class TaskAgent(BaseAgent):
    """Agent responsible for extracting structured action items from a transcript."""

    def __init__(
        self,
        name: str = "TaskAgent",
        model_name: str = "gemini-2.5-flash",
        session_service: Optional[InMemorySessionService] = None,
    ) -> None:
        """Initializes the TaskAgent and automatically loads its skill.

        Args:
            name: The name of the agent.
            model_name: The Gemini model name to use.
            session_service: Optional session service for dependency injection.
        """
        super().__init__(name=name, model_name=model_name)
        # Load skill automatically
        self.load_skill("extract_tasks")
        # Store base instruction template for formatting
        self.base_instruction: str = self.instruction
        # Dependency injection for session service
        self.session_service: InMemorySessionService = session_service or InMemorySessionService()

    def extract_tasks(self, transcript: str) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """Extracts action items from the provided meeting transcript using Gemini.

        Args:
            transcript: The transcript string to analyze.

        Returns:
            Union[List[Dict[str, Any]], Dict[str, Any]]: The structured JSON action items list,
                or an error response dictionary if validation fails.
        """
        logger.info("Starting task extraction task.")

        # Handle empty transcript
        if not transcript or not transcript.strip():
            logger.warning("Empty transcript provided.")
            return {"error": "Transcript is empty."}

        # Handle too short transcript (simple heuristic, e.g., < 15 characters)
        if len(transcript.strip()) < 15:
            logger.warning("Transcript is too short.")
            return {"error": "Transcript does not contain sufficient information."}

        # Replace template placeholder with actual transcript
        instruction_with_transcript = self.base_instruction.replace("{transcript}", transcript)
        self.instruction = instruction_with_transcript

        # Reset ADK Agent so it gets re-initialized with updated instruction
        self.adk_agent = None

        return self._execute(prompt="Please extract tasks.", session_service=self.session_service)
