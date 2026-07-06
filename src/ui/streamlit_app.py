"""MeetingMind AI Streamlit User Interface.

Provides a web-based interface for uploading meeting transcripts,
triggering multi-agent analysis, viewing structured results, and downloading JSON outputs.
"""

import sys
import logging
import json
from pathlib import Path
from typing import Dict, Any, List

import streamlit as st

# Setup sys.path to allow importing from the root 'src' directory
src_dir = Path(__file__).resolve().parent.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Configure logging for the UI component
from src.core.logging_config import setup_logging
from src.config import validate_config
from src.orchestrator.meetingmind_orchestrator import MeetingMindOrchestrator

setup_logging(level=logging.INFO)
logger = logging.getLogger("meetingmind.ui")


def display_summary(summary_data: Dict[str, Any]) -> None:
    """Renders the structured meeting summary.

    Args:
        summary_data: The JSON output from the SummaryAgent.
    """
    st.subheader(summary_data.get("meeting_title", "Meeting Summary"))
    st.write(summary_data.get("summary", "No summary provided."))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🔑 Key Decisions")
        decisions = summary_data.get("decisions", [])
        if decisions:
            for item in decisions:
                st.markdown(f"- {item}")
        else:
            st.write("None recorded.")

    with col2:
        st.markdown("### ⚠️ Risks")
        risks = summary_data.get("risks", [])
        if risks:
            for item in risks:
                st.markdown(f"- {item}")
        else:
            st.write("None recorded.")

    with col3:
        st.markdown("### 🎯 Next Steps")
        next_steps = summary_data.get("next_steps", [])
        if next_steps:
            for item in next_steps:
                st.markdown(f"- {item}")
        else:
            st.write("None recorded.")


def display_action_items(tasks: List[Dict[str, Any]]) -> None:
    """Renders the extracted action items in a table.

    Args:
        tasks: The list of tasks extracted by the TaskAgent.
    """
    st.subheader("📋 Action Items")
    if not tasks:
        st.write("No action items found.")
        return

    # Render a clean table representation of tasks
    st.table(tasks)


def display_email_draft(email_data: Dict[str, Any]) -> None:
    """Renders the generated follow-up email draft.

    Args:
        email_data: The JSON output from the EmailAgent.
    """
    st.subheader("✉️ Follow-up Email Draft")
    subject = email_data.get("subject", "No Subject")
    body = email_data.get("body", "No Body Content")

    st.text_input("Subject", value=subject, disabled=True)
    st.text_area("Body", value=body, height=300, disabled=True)


def display_evaluation(review_data: Dict[str, Any]) -> None:
    """Renders the quality evaluation report.

    Args:
        review_data: The JSON evaluation output from the ReviewerAgent.
    """
    st.subheader("🔍 Quality Evaluation Report")

    # Metrics layout
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Score", f"{review_data.get('overall_score', 0)}/100")
    with col2:
        st.metric("Summary Score", f"{review_data.get('summary_score', 0)}/100")
    with col3:
        st.metric("Task Score", f"{review_data.get('task_score', 0)}/100")
    with col4:
        st.metric("Email Score", f"{review_data.get('email_score', 0)}/100")

    st.markdown("### ⚠️ Key Issues")
    issues = review_data.get("issues", [])
    if issues:
        for issue in issues:
            st.markdown(f"- {issue}")
    else:
        st.success("No issues detected!")

    st.markdown("### 💡 Suggestions for Improvement")
    suggestions = review_data.get("suggestions", [])
    if suggestions:
        for suggestion in suggestions:
            st.markdown(f"- {suggestion}")
    else:
        st.write("No suggestions.")


def main() -> None:
    """Streamlit Application Entrypoint."""
    st.set_page_config(page_title="MeetingMind AI", page_icon="🧠", layout="wide")

    st.title("MeetingMind AI")
    st.caption("Google ADK Multi-Agent Meeting Assistant")

    # Validate configurations
    if not validate_config():
        st.error("Missing configuration: GEMINI_API_KEY environment variable is not set.")
        logger.error("Configuration validation failed on startup.")
        return

    # File Uploader
    uploaded_file = st.file_uploader("Upload meeting transcript (.txt)", type=["txt"])

    if uploaded_file is not None:
        transcript_content = uploaded_file.read().decode("utf-8")

        # Analyze button
        if st.button("Analyze", type="primary"):
            logger.info("Analyze button clicked for file: %s", uploaded_file.name)
            with st.spinner("Analyzing meeting transcript..."):
                try:
                    orchestrator = MeetingMindOrchestrator()
                    results = orchestrator.process_meeting(transcript_content)

                    if isinstance(results, dict) and "error" in results:
                        st.error(f"Error during processing: {results['error']}")
                        logger.error("Orchestrator returned error: %s", results["error"])
                    else:
                        st.session_state["results"] = results
                        st.session_state["filename"] = uploaded_file.name
                        st.success("Analysis complete!")
                        logger.info("Successfully completed processing for %s", uploaded_file.name)
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
                    logger.exception("Unexpected error in Streamlit UI run loop")

    # Render results if available in session state
    if "results" in st.session_state:
        results = st.session_state["results"]

        st.divider()

        # Display results structured in tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Meeting Summary", "Action Items", "Email Draft", "Evaluation"])

        with tab1:
            display_summary(results.get("summary", {}))

        with tab2:
            display_action_items(results.get("tasks", []))

        with tab3:
            display_email_draft(results.get("email", {}))

        with tab4:
            display_evaluation(results.get("review", {}))

        st.divider()

        # Download button
        json_string = json.dumps(results, indent=2)
        st.download_button(
            label="Download JSON Results",
            data=json_string,
            file_name=f"{st.session_state['filename']}_analysis.json",
            mime="application/json"
        )


if __name__ == "__main__":
    main()
