"""Unit tests for the TaskAgent class using the built-in unittest framework."""

import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from google.adk.sessions import InMemorySessionService

# Ensure src directory is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from agents.task_agent import TaskAgent


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
        self.author = "TaskAgent"


class TestTaskAgent(unittest.TestCase):
    """Test suite for TaskAgent class."""

    def setUp(self) -> None:
        """Sets up a TaskAgent instance for testing."""
        self.session_service = InMemorySessionService()
        self.task_agent = TaskAgent(session_service=self.session_service)

    def test_extract_tasks_empty_transcript(self) -> None:
        """Negative test: verify handling of an empty transcript."""
        result = self.task_agent.extract_tasks("")
        self.assertEqual(result, {"error": "Transcript is empty."})

        result_whitespace = self.task_agent.extract_tasks("   \n  ")
        self.assertEqual(result_whitespace, {"error": "Transcript is empty."})

    def test_extract_tasks_too_short_transcript(self) -> None:
        """Negative test: verify handling of a transcript that is too short."""
        result = self.task_agent.extract_tasks("Short")
        self.assertEqual(result, {"error": "Transcript does not contain sufficient information."})

    @patch("google.adk.Runner.run_debug", new_callable=AsyncMock)
    def test_extract_tasks_success(self, mock_run_debug: AsyncMock) -> None:
        """Positive test: verify successful task extraction."""
        mock_json_response = """
        [
          {
            "task": "Prepare UI mockups",
            "owner": "Raxit",
            "deadline": "Friday",
            "priority": "High"
          },
          {
            "task": "Review documentation",
            "owner": "Neha",
            "deadline": "Wednesday",
            "priority": "Medium"
          }
        ]
        """
        mock_run_debug.return_value = [MockEvent(mock_json_response)]

        transcript = "Raxit will prepare the UI mockups by Friday. Neha needs to review documentation by Wednesday."
        result = self.task_agent.extract_tasks(transcript)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["task"], "Prepare UI mockups")
        self.assertEqual(result[0]["owner"], "Raxit")
        self.assertEqual(result[0]["deadline"], "Friday")
        self.assertEqual(result[0]["priority"], "High")

    @patch("google.adk.Runner.run_debug", new_callable=AsyncMock)
    def test_extract_tasks_invalid_json(self, mock_run_debug: AsyncMock) -> None:
        """Negative test: verify handling of an invalid/non-JSON response from model."""
        mock_run_debug.return_value = [MockEvent("This is not JSON")]

        transcript = "Raxit will prepare the UI mockups by Friday."
        result = self.task_agent.extract_tasks(transcript)

        self.assertEqual(result, {"error": "Transcript could not be processed."})

    @patch("google.adk.Runner.run_debug", new_callable=AsyncMock)
    def test_extract_tasks_api_error(self, mock_run_debug: AsyncMock) -> None:
        """Negative test: verify handling of API/runtime exceptions."""
        mock_run_debug.side_effect = Exception("API connection timed out")

        transcript = "Raxit will prepare the UI mockups by Friday."
        result = self.task_agent.extract_tasks(transcript)

        self.assertEqual(result, {"error": "Transcript could not be processed."})


if __name__ == "__main__":
    unittest.main()
