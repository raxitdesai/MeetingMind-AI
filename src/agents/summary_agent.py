"""Summary Agent implementation for MeetingMind AI.

This module implements the SummaryAgent which inherits from BaseAgent.
It automatically loads instructions from the summarize/SKILL.md file,
initializes the Google ADK Agent, and uses it to summarize meeting transcripts.
"""

import logging
from typing import Optional, Dict, Any

from google.adk.sessions import InMemorySessionService
from agents.base_agent import BaseAgent

logger = logging.getLogger("meetingmind.agents.summary")


class SummaryAgent(BaseAgent):
    """Agent responsible for producing a structured meeting summary from a transcript."""

    def __init__(
        self,
        name: str = "SummaryAgent",
        model_name: str = "gemini-2.5-flash",
        session_service: Optional[InMemorySessionService] = None,
    ) -> None:
        """Initializes the SummaryAgent and automatically loads its skill.

        Args:
            name: The name of the agent.
            model_name: The Gemini model name to use.
            session_service: Optional session service for dependency injection.
        """
        super().__init__(name=name, model_name=model_name)
        # Load skill automatically
        self.load_skill("summarize")
        # Store base instruction template for formatting
        self.base_instruction: str = self.instruction
        # Dependency injection for session service
        self.session_service: InMemorySessionService = session_service or InMemorySessionService()

    def summarize(self, transcript: str) -> Dict[str, Any]:
        """Summarizes the provided meeting transcript using Gemini.

        Args:
            transcript: The transcript string to analyze.

        Returns:
            Dict[str, Any]: The structured JSON meeting summary or error response.
        """
        logger.info("Starting summarization task.")

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

        return self._execute(prompt="Please summarize.", session_service=self.session_service)
