"""Unit tests for the EmailAgent class using the built-in unittest framework."""

import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from google.adk.sessions import InMemorySessionService

# Ensure src directory is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from src.agents.email_agent import EmailAgent


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
        self.author = "EmailAgent"


class TestEmailAgent(unittest.TestCase):
    """Test suite for EmailAgent class."""

    def setUp(self) -> None:
        """Sets up an EmailAgent instance for testing."""
        self.session_service = InMemorySessionService()
        self.email_agent = EmailAgent(session_service=self.session_service)

    def test_generate_email_missing_summary(self) -> None:
        """Negative test: verify handling when summary is missing (None)."""
        result = self.email_agent.generate_email(None, [{"task": "Do something"}])
        self.assertEqual(result, {"error": "Summary is missing."})

    def test_generate_email_missing_tasks(self) -> None:
        """Negative test: verify handling when tasks list is missing (None)."""
        result = self.email_agent.generate_email({"meeting_title": "Title"}, None)
        self.assertEqual(result, {"error": "Tasks are missing."})

    def test_generate_email_empty_summary(self) -> None:
        """Negative test: verify handling when summary is empty dict."""
        result = self.email_agent.generate_email({}, [{"task": "Do something"}])
        self.assertEqual(result, {"error": "Summary is empty."})

    def test_generate_email_empty_tasks(self) -> None:
        """Negative test: verify handling when tasks list is empty list."""
        result = self.email_agent.generate_email({"meeting_title": "Title"}, [])
        self.assertEqual(result, {"error": "Task list is empty."})

    @patch("google.adk.Runner.run_debug", new_callable=AsyncMock)
    def test_generate_email_success(self, mock_run_debug: AsyncMock) -> None:
        """Positive test: verify successful follow-up email generation."""
        mock_json_response = """
        {
          "subject": "Follow-up: Project Kickoff Meeting",
          "body": "Hi team, here is the summary of the kickoff meeting..."
        }
        """
        mock_run_debug.return_value = [MockEvent(mock_json_response)]

        summary = {
            "meeting_title": "Project Kickoff Meeting",
            "summary": "We discussed project timelines."
        }
        tasks = [
            {
                "task": "Prepare UI mockups",
                "owner": "Raxit",
                "deadline": "Friday",
                "priority": "High"
            }
        ]

        result = self.email_agent.generate_email(summary, tasks)

        self.assertIsInstance(result, dict)
        self.assertEqual(result["subject"], "Follow-up: Project Kickoff Meeting")
        self.assertEqual(result["body"], "Hi team, here is the summary of the kickoff meeting...")

    @patch("google.adk.Runner.run_debug", new_callable=AsyncMock)
    def test_generate_email_invalid_json(self, mock_run_debug: AsyncMock) -> None:
        """Negative test: verify handling of an invalid/non-JSON response from model."""
        mock_run_debug.return_value = [MockEvent("This is not JSON")]

        summary = {"meeting_title": "Kickoff"}
        tasks = [{"task": "Do something"}]
        result = self.email_agent.generate_email(summary, tasks)

        self.assertEqual(result, {"error": "Transcript could not be processed."})

    @patch("google.adk.Runner.run_debug", new_callable=AsyncMock)
    def test_generate_email_api_error(self, mock_run_debug: AsyncMock) -> None:
        """Negative test: verify handling of API/runtime exceptions."""
        mock_run_debug.side_effect = Exception("API connection timed out")

        summary = {"meeting_title": "Kickoff"}
        tasks = [{"task": "Do something"}]
        result = self.email_agent.generate_email(summary, tasks)

        self.assertEqual(result, {"error": "Transcript could not be processed."})


if __name__ == "__main__":
    unittest.main()
