"""Unit tests for the ReviewerAgent class using the built-in unittest framework."""

import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from google.adk.sessions import InMemorySessionService

# Ensure src directory is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from src.agents.reviewer_agent import ReviewerAgent


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
        self.author = "ReviewerAgent"


class TestReviewerAgent(unittest.TestCase):
    """Test suite for ReviewerAgent class."""

    def setUp(self) -> None:
        """Sets up a ReviewerAgent instance for testing."""
        self.session_service = InMemorySessionService()
        self.reviewer_agent = ReviewerAgent(session_service=self.session_service)

    def test_evaluate_missing_summary(self) -> None:
        """Negative test: verify handling when summary is missing (None)."""
        result = self.reviewer_agent.evaluate(
            None,
            [{"task": "Do something"}],
            {"subject": "Subj", "body": "Body"}
        )
        self.assertEqual(result, {"error": "Summary is missing."})

    def test_evaluate_missing_tasks(self) -> None:
        """Negative test: verify handling when tasks list is missing (None)."""
        result = self.reviewer_agent.evaluate(
            {"meeting_title": "Title"},
            None,
            {"subject": "Subj", "body": "Body"}
        )
        self.assertEqual(result, {"error": "Tasks are missing."})

    def test_evaluate_missing_email(self) -> None:
        """Negative test: verify handling when email is missing (None)."""
        result = self.reviewer_agent.evaluate(
            {"meeting_title": "Title"},
            [{"task": "Do something"}],
            None
        )
        self.assertEqual(result, {"error": "Email is missing."})

    def test_evaluate_empty_summary(self) -> None:
        """Negative test: verify handling when summary is empty dict."""
        result = self.reviewer_agent.evaluate(
            {},
            [{"task": "Do something"}],
            {"subject": "Subj", "body": "Body"}
        )
        self.assertEqual(result, {"error": "Summary is empty."})

    def test_evaluate_empty_tasks(self) -> None:
        """Negative test: verify handling when tasks list is empty list."""
        result = self.reviewer_agent.evaluate(
            {"meeting_title": "Title"},
            [],
            {"subject": "Subj", "body": "Body"}
        )
        self.assertEqual(result, {"error": "Tasks are empty."})

    def test_evaluate_empty_email(self) -> None:
        """Negative test: verify handling when email is empty dict."""
        result = self.reviewer_agent.evaluate(
            {"meeting_title": "Title"},
            [{"task": "Do something"}],
            {}
        )
        self.assertEqual(result, {"error": "Email is empty."})

    @patch("google.adk.Runner.run_debug", new_callable=AsyncMock)
    def test_evaluate_success(self, mock_run_debug: AsyncMock) -> None:
        """Positive test: verify successful evaluation report generation."""
        mock_json_response = """
        {
          "overall_score": 95,
          "summary_score": 95,
          "task_score": 95,
          "email_score": 95,
          "issues": [],
          "suggestions": []
        }
        """
        mock_run_debug.return_value = [MockEvent(mock_json_response)]

        summary = {
            "meeting_title": "Kickoff",
            "summary": "Timelines discussed."
        }
        tasks = [
            {
                "task": "Prepare UI mockups",
                "owner": "Raxit",
                "deadline": "Friday",
                "priority": "High"
            }
        ]
        email = {
            "subject": "Follow-up",
            "body": "Body text"
        }

        result = self.reviewer_agent.evaluate(summary, tasks, email)

        self.assertIsInstance(result, dict)
        self.assertEqual(result["overall_score"], 95)
        self.assertEqual(result["summary_score"], 95)
        self.assertEqual(result["task_score"], 95)
        self.assertEqual(result["email_score"], 95)
        self.assertEqual(result["issues"], [])
        self.assertEqual(result["suggestions"], [])

    @patch("google.adk.Runner.run_debug", new_callable=AsyncMock)
    def test_evaluate_invalid_json(self, mock_run_debug: AsyncMock) -> None:
        """Negative test: verify handling of an invalid/non-JSON response from model."""
        mock_run_debug.return_value = [MockEvent("This is not JSON")]

        summary = {"meeting_title": "Kickoff"}
        tasks = [{"task": "Do something"}]
        email = {"subject": "Subj", "body": "Body"}
        result = self.reviewer_agent.evaluate(summary, tasks, email)

        self.assertEqual(result, {"error": "Transcript could not be processed."})

    @patch("google.adk.Runner.run_debug", new_callable=AsyncMock)
    def test_evaluate_api_error(self, mock_run_debug: AsyncMock) -> None:
        """Negative test: verify handling of API/runtime exceptions."""
        mock_run_debug.side_effect = Exception("API connection timed out")

        summary = {"meeting_title": "Kickoff"}
        tasks = [{"task": "Do something"}]
        email = {"subject": "Subj", "body": "Body"}
        result = self.reviewer_agent.evaluate(summary, tasks, email)

        self.assertEqual(result, {"error": "Transcript could not be processed."})


if __name__ == "__main__":
    unittest.main()
