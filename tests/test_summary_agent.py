"""Unit tests for the SummaryAgent class using the built-in unittest framework."""

import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from google.adk.sessions import InMemorySessionService

# Ensure src directory is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from src.agents.summary_agent import SummaryAgent


class MockPart:
    """Mock for Google ADK Part."""
    def __init__(self, text: str) -> None:
        self.text = text


class MockContent:
    """Mock for Google ADK Content."""
    def __init__(self, text: str) -> None:
        self.parts = [MockPart(text)]


class MockEvent:
    """Mock for Google ADK Event."""
    def __init__(self, text: str) -> None:
        self.content = MockContent(text)
        self.id = "mock-event-id"
        self.author = "SummaryAgent"


class TestSummaryAgent(unittest.TestCase):
    """Test suite for SummaryAgent class."""

    def setUp(self) -> None:
        """Sets up a SummaryAgent instance for testing."""
        self.session_service = InMemorySessionService()
        self.summary_agent = SummaryAgent(session_service=self.session_service)

    def test_summarize_empty_transcript(self) -> None:
        """Negative test: verify handling of an empty transcript."""
        result = self.summary_agent.summarize("")
        self.assertEqual(result, {"error": "Transcript is empty."})

        result_whitespace = self.summary_agent.summarize("   \n  ")
        self.assertEqual(result_whitespace, {"error": "Transcript is empty."})

    def test_summarize_too_short_transcript(self) -> None:
        """Negative test: verify handling of a transcript that is too short."""
        result = self.summary_agent.summarize("Short")
        self.assertEqual(result, {"error": "Transcript does not contain sufficient information."})

    @patch("google.adk.Runner.run_debug", new_callable=AsyncMock)
    def test_summarize_success(self, mock_run_debug: AsyncMock) -> None:
        """Positive test: verify successful summarization."""
        mock_json_response = """
        {
          "meeting_title": "Project Kickoff Meeting",
          "meeting_date": "Not mentioned",
          "participants": ["Raxit", "Neha", "Jumkhi"],
          "summary": "Team kickoff meeting to discuss launching MeetingMind AI.",
          "decisions": ["Proceed with the launch of MeetingMind AI."],
          "risks": ["Not mentioned"],
          "next_steps": ["Raxit will prepare the UI by Friday."]
        }
        """
        mock_run_debug.return_value = [MockEvent(mock_json_response)]

        transcript = "Project Kickoff Meeting\nParticipants: Raxit, Neha, Jumkhi\nDiscussion: Launch MeetingMind AI MVP."
        result = self.summary_agent.summarize(transcript)

        self.assertEqual(result["meeting_title"], "Project Kickoff Meeting")
        self.assertIn("Raxit", result["participants"])
        self.assertEqual(result["summary"], "Team kickoff meeting to discuss launching MeetingMind AI.")
        self.assertNotIn("error", result)

    @patch("google.adk.Runner.run_debug", new_callable=AsyncMock)
    def test_summarize_invalid_json(self, mock_run_debug: AsyncMock) -> None:
        """Negative test: verify handling of an invalid/non-JSON response from model."""
        mock_run_debug.return_value = [MockEvent("This is not JSON")]

        transcript = "Project Kickoff Meeting\nParticipants: Raxit, Neha, Jumkhi\nDiscussion: Launch MeetingMind AI MVP."
        result = self.summary_agent.summarize(transcript)

        self.assertEqual(result, {"error": "Transcript could not be processed."})

    @patch("google.adk.Runner.run_debug", new_callable=AsyncMock)
    def test_summarize_api_error(self, mock_run_debug: AsyncMock) -> None:
        """Negative test: verify handling of API/runtime exceptions."""
        mock_run_debug.side_effect = Exception("API connection timed out")

        transcript = "Project Kickoff Meeting\nParticipants: Raxit, Neha, Jumkhi\nDiscussion: Launch MeetingMind AI MVP."
        result = self.summary_agent.summarize(transcript)

        self.assertEqual(result, {"error": "Transcript could not be processed."})


if __name__ == "__main__":
    unittest.main()
