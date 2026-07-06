# PROJECT_ARCHITECTURE.md

# MeetingMind AI -- Architecture Document

**Version:** 1.0\
**Project:** MeetingMind AI\
**Purpose:** Technical Architecture Reference for the Google × Kaggle AI
Agents Capstone Project

------------------------------------------------------------------------

# 1. Executive Summary

MeetingMind AI is a modular multi-agent application that converts
meeting transcripts into structured business outputs using Google Agent
Development Kit (ADK), Gemini models, Model Context Protocol (MCP),
reusable Agent Skills, and a Streamlit user interface.

The system intentionally separates responsibilities into specialized AI
agents coordinated by a central orchestrator. This demonstrates modern
AI engineering practices including modularity, orchestration, reusable
prompting, secure configuration, evaluation, and local deployability.

------------------------------------------------------------------------

# 2. Business Problem

After meetings, teams spend time manually creating summaries, extracting
action items, drafting follow-up emails, and validating meeting
outcomes. This repetitive work delays execution and often leads to
missed decisions.

MeetingMind AI automates these activities while preserving a clear and
extensible architecture.

------------------------------------------------------------------------

# 3. Solution Overview

The solution processes a transcript through four specialized AI agents:

1.  SummaryAgent
2.  TaskAgent
3.  EmailAgent
4.  ReviewerAgent

A MeetingMindOrchestrator coordinates the workflow and aggregates the
results into a single structured response.

------------------------------------------------------------------------

# 4. Design Goals

-   Modular architecture
-   Separation of concerns
-   Reusable prompt skills
-   Secure configuration
-   Local deployment
-   Simple extensibility
-   Testability

------------------------------------------------------------------------

# 5. High-Level Architecture

``` mermaid
flowchart TD
User --> UI["Streamlit UI"]
UI --> ORCH["MeetingMind Orchestrator"]
ORCH --> SA["SummaryAgent"]
ORCH --> TA["TaskAgent"]
ORCH --> EA["EmailAgent"]
ORCH --> RA["ReviewerAgent"]
SA --> ADK["Google ADK"]
TA --> ADK
EA --> ADK
RA --> ADK
ADK --> GEMINI["Gemini Model"]
ORCH --> MCP["Filesystem MCP Client"]
MCP --> SERVER["Filesystem MCP Server"]
SERVER --> FILES["Local Files"]
```

------------------------------------------------------------------------

# 6. Component Architecture

## Streamlit UI

Responsible for user interaction, transcript upload, and displaying
results.

## MeetingMind Orchestrator

Coordinates all agents, manages workflow sequencing, and returns
consolidated output.

## AI Agents

### SummaryAgent

Produces an executive summary.

### TaskAgent

Extracts action items and ownership.

### EmailAgent

Generates a professional follow-up email.

### ReviewerAgent

Evaluates completeness and quality of generated content.

------------------------------------------------------------------------

# 7. Agent Collaboration

``` mermaid
flowchart LR
Transcript --> Summary --> Tasks --> Email --> Review --> JSON
```

Each agent performs one responsibility, improving maintainability and
simplifying testing.

------------------------------------------------------------------------

# 8. Agent Skills

Prompt instructions are maintained as external SKILL.md files.

Benefits:

-   Prompt reuse
-   Easier maintenance
-   Clear separation between prompting and application logic

------------------------------------------------------------------------

# 9. MCP Integration

MeetingMind AI demonstrates Model Context Protocol (MCP) by delegating
file operations through an MCP client communicating with a filesystem
MCP server.

Benefits include:

-   Standardized tool interface
-   Separation from application logic
-   Future extensibility

------------------------------------------------------------------------

# 10. Security Model

Security considerations include:

-   API keys stored in .env
-   No hardcoded secrets
-   Input validation
-   Structured logging
-   Exception handling
-   Local-first execution

------------------------------------------------------------------------

# 11. Deployability

Deployment requires only:

-   Python 3.11+
-   requirements.txt
-   Gemini API key

Run:

``` bash
python -m streamlit run src/ui/streamlit_app.py
```

------------------------------------------------------------------------

# 12. Testing Strategy

The project includes:

-   Unit tests
-   Orchestrator validation
-   MCP verification
-   End-to-end workflow validation
-   Streamlit UI verification

------------------------------------------------------------------------

# 13. Engineering Decisions

  Decision             Rationale
  -------------------- --------------------------------
  Multi-agent design   Separation of responsibilities
  Orchestrator         Centralized workflow
  Agent Skills         Prompt reuse
  MCP                  Standard protocol integration
  Streamlit            Lightweight deployment
  Local execution      Simplicity and privacy

------------------------------------------------------------------------

# 14. Trade-offs

Advantages:

-   Easy to extend
-   Easy to test
-   Clear architecture
-   Reusable skills

Limitations:

-   Sequential execution
-   Local deployment only
-   Depends on Gemini API availability

------------------------------------------------------------------------

# 15. Future Roadmap

-   Calendar integration
-   Email delivery
-   Audio transcription
-   Cloud deployment
-   RAG integration
-   Analytics dashboard
-   Additional specialized agents

------------------------------------------------------------------------

# 16. Mapping to Kaggle Evaluation

  Evaluation Concept   Evidence
  -------------------- ----------------------------
  Google ADK           Specialized agents
  Multi-Agent          Four collaborating agents
  MCP                  Filesystem MCP integration
  Agent Skills         External SKILL.md
  Security             .env, validation, logging
  Deployability        Streamlit
  Antigravity          Development workflow
  Evaluation           ReviewerAgent

------------------------------------------------------------------------

# 17. Lessons Learned

-   Multi-agent systems improve modularity.
-   AI-generated code still requires architecture review.
-   Early integration testing prevents late-stage issues.
-   External Agent Skills reduce prompt duplication.
-   Central orchestration simplifies UI and testing.

------------------------------------------------------------------------

# 18. Conclusion

MeetingMind AI demonstrates the practical application of Google ADK,
MCP, Agent Skills, and multi-agent orchestration in a realistic business
scenario.

The project intentionally favors clarity, modularity, and
maintainability over unnecessary complexity, making it suitable as both
a Kaggle capstone submission and a portfolio project.
