"""Unit tests for MeetingMindOrchestrator."""

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

# Ensure src directory is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from orchestrator.meetingmind_orchestrator import MeetingMindOrchestrator


class TestMeetingMindOrchestrator(unittest.TestCase):
    """Test suite for MeetingMindOrchestrator class."""

    def setUp(self) -> None:
        """Sets up mock agents and the orchestrator instance for testing."""
        self.mock_summary_agent = MagicMock()
        self.mock_task_agent = MagicMock()
        self.mock_email_agent = MagicMock()
        self.mock_reviewer_agent = MagicMock()

        self.orchestrator = MeetingMindOrchestrator(
            summary_agent=self.mock_summary_agent,
            task_agent=self.mock_task_agent,
            email_agent=self.mock_email_agent,
            reviewer_agent=self.mock_reviewer_agent,
        )
        self.transcript = "Test meeting transcript content."

        # Setup default successful return values
        self.mock_summary_val = {
            "meeting_title": "Test Title",
            "summary": "Test Summary",
            "decisions": [],
            "risks": [],
            "next_steps": []
        }
        self.mock_task_val = [
            {
                "task": "Test Task",
                "owner": "Test Owner",
                "deadline": "Test Deadline",
                "priority": "High"
            }
        ]
        self.mock_email_val = {
            "subject": "Test Subject",
            "body": "Test Body"
        }
        self.mock_reviewer_val = {
            "overall_score": 95,
            "summary_score": 96,
            "task_score": 92,
            "email_score": 97,
            "issues": [],
            "suggestions": []
        }

    def test_process_meeting_success(self) -> None:
        """Verify successful end-to-end orchestration workflow."""
        self.mock_summary_agent.summarize.return_value = self.mock_summary_val
        self.mock_task_agent.extract_tasks.return_value = self.mock_task_val
        self.mock_email_agent.generate_email.return_value = self.mock_email_val
        self.mock_reviewer_agent.evaluate.return_value = self.mock_reviewer_val

        result = self.orchestrator.process_meeting(self.transcript)

        self.assertIsInstance(result, dict)
        self.assertIn("summary", result)
        self.assertIn("tasks", result)
        self.assertIn("email", result)
        self.assertIn("review", result)
        self.assertEqual(result["summary"], self.mock_summary_val)
        self.assertEqual(result["tasks"], self.mock_task_val)
        self.assertEqual(result["email"], self.mock_email_val)
        self.assertEqual(result["review"], self.mock_reviewer_val)

        # Verify call arguments
        self.mock_summary_agent.summarize.assert_called_once_with(self.transcript)
        self.mock_task_agent.extract_tasks.assert_called_once_with(self.transcript)
        self.mock_email_agent.generate_email.assert_called_once_with(
            self.mock_summary_val, self.mock_task_val
        )
        self.mock_reviewer_agent.evaluate.assert_called_once_with(
            self.mock_summary_val, self.mock_task_val, self.mock_email_val
        )

    def test_process_meeting_summary_failure(self) -> None:
        """Verify workflow stops and returns error if SummaryAgent fails."""
        expected_error = {"error": "Summary failed"}
        self.mock_summary_agent.summarize.return_value = expected_error

        result = self.orchestrator.process_meeting(self.transcript)

        self.assertEqual(result, expected_error)
        self.mock_summary_agent.summarize.assert_called_once_with(self.transcript)
        self.mock_task_agent.extract_tasks.assert_not_called()
        self.mock_email_agent.generate_email.assert_not_called()
        self.mock_reviewer_agent.evaluate.assert_not_called()

    def test_process_meeting_task_failure(self) -> None:
        """Verify workflow stops and returns error if TaskAgent fails."""
        expected_error = {"error": "Task extraction failed"}
        self.mock_summary_agent.summarize.return_value = self.mock_summary_val
        self.mock_task_agent.extract_tasks.return_value = expected_error

        result = self.orchestrator.process_meeting(self.transcript)

        self.assertEqual(result, expected_error)
        self.mock_summary_agent.summarize.assert_called_once_with(self.transcript)
        self.mock_task_agent.extract_tasks.assert_called_once_with(self.transcript)
        self.mock_email_agent.generate_email.assert_not_called()
        self.mock_reviewer_agent.evaluate.assert_not_called()

    def test_process_meeting_email_failure(self) -> None:
        """Verify workflow stops and returns error if EmailAgent fails."""
        expected_error = {"error": "Email drafting failed"}
        self.mock_summary_agent.summarize.return_value = self.mock_summary_val
        self.mock_task_agent.extract_tasks.return_value = self.mock_task_val
        self.mock_email_agent.generate_email.return_value = expected_error

        result = self.orchestrator.process_meeting(self.transcript)

        self.assertEqual(result, expected_error)
        self.mock_summary_agent.summarize.assert_called_once_with(self.transcript)
        self.mock_task_agent.extract_tasks.assert_called_once_with(self.transcript)
        self.mock_email_agent.generate_email.assert_called_once_with(
            self.mock_summary_val, self.mock_task_val
        )
        self.mock_reviewer_agent.evaluate.assert_not_called()

    def test_process_meeting_reviewer_failure(self) -> None:
        """Verify workflow stops and returns error if ReviewerAgent fails."""
        expected_error = {"error": "Evaluation failed"}
        self.mock_summary_agent.summarize.return_value = self.mock_summary_val
        self.mock_task_agent.extract_tasks.return_value = self.mock_task_val
        self.mock_email_agent.generate_email.return_value = self.mock_email_val
        self.mock_reviewer_agent.evaluate.return_value = expected_error

        result = self.orchestrator.process_meeting(self.transcript)

        self.assertEqual(result, expected_error)
        self.mock_summary_agent.summarize.assert_called_once_with(self.transcript)
        self.mock_task_agent.extract_tasks.assert_called_once_with(self.transcript)
        self.mock_email_agent.generate_email.assert_called_once_with(
            self.mock_summary_val, self.mock_task_val
        )
        self.mock_reviewer_agent.evaluate.assert_called_once_with(
            self.mock_summary_val, self.mock_task_val, self.mock_email_val
        )


if __name__ == "__main__":
    unittest.main()
