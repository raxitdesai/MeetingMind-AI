"""Summary Agent implementation for MeetingMind AI.

This module implements the SummaryAgent which inherits from BaseAgent.
It automatically loads instructions from the summarize/SKILL.md file,
initializes the Google ADK Agent, and uses it to summarize meeting transcripts.
"""

import json
import logging
import asyncio
from typing import Optional, Dict, Any

from google.adk import Runner
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

        try:
            # Re-initialize the ADK Agent with the updated instruction containing the transcript
            self.initialize_adk_agent()

            runner = Runner(
                agent=self.adk_agent,
                app_name="meetingmind_app",
                session_service=self.session_service
            )

            # Invoke the agent asynchronously and wait for the results
            logger.info("Invoking Gemini via ADK runner...")
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            if loop.is_running():
                events = loop.run_until_complete(runner.run_debug("Please summarize."))
            else:
                events = asyncio.run(runner.run_debug("Please summarize."))

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
            summary_data: Dict[str, Any] = json.loads(response_text)
            logger.info("Successfully parsed meeting summary response.")
            return summary_data

        except json.JSONDecodeError as je:
            logger.error("Failed to parse response as JSON: %s. Response content: %s", je, response_text)
            return {"error": "Transcript could not be processed."}
        except Exception as e:
            logger.error("Error occurred during transcript summarization: %s", e, exc_info=True)
            return {"error": "Transcript could not be processed."}
