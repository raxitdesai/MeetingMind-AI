"""MeetingMind AI Orchestrator implementation.

This module provides the MeetingMindOrchestrator class which coordinates the sequential
execution of all agents: SummaryAgent, TaskAgent, EmailAgent, and ReviewerAgent.
It supports dependency injection for agent instances to facilitate mocking during testing.
"""

import logging
from typing import Optional, Dict, Any, Union

from agents.summary_agent import SummaryAgent
from agents.task_agent import TaskAgent
from agents.email_agent import EmailAgent
from agents.reviewer_agent import ReviewerAgent

logger = logging.getLogger("meetingmind.orchestrator")


class MeetingMindOrchestrator:
    """Orchestrates the sequential flow of meeting transcript processing across agents.

    Attributes:
        summary_agent: The agent used to produce meeting summaries.
        task_agent: The agent used to extract tasks.
        email_agent: The agent used to generate follow-up email drafts.
        reviewer_agent: The agent used to evaluate output quality.
    """

    def __init__(
        self,
        summary_agent: Optional[SummaryAgent] = None,
        task_agent: Optional[TaskAgent] = None,
        email_agent: Optional[EmailAgent] = None,
        reviewer_agent: Optional[ReviewerAgent] = None,
    ) -> None:
        """Initializes the orchestrator with agents, supporting dependency injection.

        Args:
            summary_agent: Optional injected SummaryAgent instance.
            task_agent: Optional injected TaskAgent instance.
            email_agent: Optional injected EmailAgent instance.
            reviewer_agent: Optional injected ReviewerAgent instance.
        """
        self.summary_agent: SummaryAgent = summary_agent or SummaryAgent()
        self.task_agent: TaskAgent = task_agent or TaskAgent()
        self.email_agent: EmailAgent = email_agent or EmailAgent()
        self.reviewer_agent: ReviewerAgent = reviewer_agent or ReviewerAgent()
        logger.info("MeetingMindOrchestrator initialized successfully.")

    def process_meeting(self, transcript: str) -> Dict[str, Any]:
        """Runs the entire sequential orchestration workflow on a transcript.

        Workflow steps:
        1. Generate meeting summary.
        2. Extract action items.
        3. Generate follow-up email draft.
        4. Evaluate outputs.

        If any agent returns an error dictionary (containing an 'error' key),
        the execution is immediately stopped, and the error dictionary is returned.

        Args:
            transcript: The raw meeting transcript string to process.

        Returns:
            Dict[str, Any]: A dictionary containing the individual outputs of all steps,
                structured as follows:
                {
                    "summary": Dict[str, Any],
                    "tasks": List[Dict[str, Any]],
                    "email": Dict[str, Any],
                    "review": Dict[str, Any]
                }
                Or the error dictionary returned by the failing agent.
        """
        logger.info("Processing meeting transcript...")

        # Stage 1: Summarize
        logger.info("Stage 1: Generating meeting summary...")
        summary = self.summary_agent.summarize(transcript)
        if isinstance(summary, dict) and "error" in summary:
            logger.error("Stage 1 failed with error: %s", summary["error"])
            return summary

        # Stage 2: Extract tasks
        logger.info("Stage 2: Extracting action items...")
        tasks = self.task_agent.extract_tasks(transcript)
        if isinstance(tasks, dict) and "error" in tasks:
            logger.error("Stage 2 failed with error: %s", tasks["error"])
            return tasks

        # Stage 3: Generate email follow-up
        logger.info("Stage 3: Generating email draft...")
        email = self.email_agent.generate_email(summary, tasks)
        if isinstance(email, dict) and "error" in email:
            logger.error("Stage 3 failed with error: %s", email["error"])
            return email

        # Stage 4: Evaluate results
        logger.info("Stage 4: Evaluating agent outputs...")
        review = self.reviewer_agent.evaluate(summary, tasks, email)
        if isinstance(review, dict) and "error" in review:
            logger.error("Stage 4 failed with error: %s", review["error"])
            return review

        logger.info("Meeting transcript processing successfully completed.")
        return {
            "summary": summary,
            "tasks": tasks,
            "email": email,
            "review": review,
        }
