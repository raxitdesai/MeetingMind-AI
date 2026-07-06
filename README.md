# 🧠 MeetingMind AI

> **Multi-Agent Meeting Intelligence powered by Google Agent Development
> Kit (ADK), Gemini, Model Context Protocol (MCP), and Streamlit**

![Python](https://img.shields.io/badge/Python-3.11+-blue) ![Google
ADK](https://img.shields.io/badge/Google-ADK-green)
![Gemini](https://img.shields.io/badge/LLM-Gemini-orange)
![MCP](https://img.shields.io/badge/Protocol-MCP-purple)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

------------------------------------------------------------------------

## Overview

MeetingMind AI transforms unstructured meeting transcripts into
structured business outcomes using a coordinated **multi-agent
architecture**.

Instead of relying on one large prompt, the solution delegates
responsibilities to specialized AI agents coordinated by an
orchestrator.

Outputs include:

-   Executive meeting summary
-   Action items with owners
-   Professional follow-up email
-   AI quality review
-   Structured JSON output

The project demonstrates modern AI engineering concepts taught in the
**Google × Kaggle AI Agents: Intensive Vibe Coding Course**.

------------------------------------------------------------------------

# Problem Statement

Organizations spend significant time after meetings:

-   Writing summaries
-   Identifying action items
-   Preparing follow-up emails
-   Reviewing meeting outcomes

MeetingMind AI automates this workflow using specialized AI agents.

------------------------------------------------------------------------

# Why AI Agents?

Meeting processing naturally decomposes into separate responsibilities.

  Agent           Responsibility
  --------------- ----------------------------
  SummaryAgent    Meeting summary
  TaskAgent       Extract action items
  EmailAgent      Draft follow-up email
  ReviewerAgent   Evaluate generated outputs

A central **MeetingMind Orchestrator** coordinates these agents.

------------------------------------------------------------------------

# Key Features

-   Multi-Agent Architecture
-   Google ADK based agents
-   Gemini integration
-   MCP-enabled file interaction
-   Reusable Agent Skills
-   Streamlit UI
-   JSON export
-   Local-first deployment
-   Unit-tested components

------------------------------------------------------------------------

# Engineering Highlights

  Decision               Benefit
  ---------------------- -----------------------------------
  Specialized Agents     Separation of concerns
  Orchestrator Pattern   Central workflow coordination
  Agent Skills           Prompt reuse
  MCP Integration        Standardized external interaction
  Streamlit              Rapid deployment
  Local execution        Simplicity and privacy

------------------------------------------------------------------------

# High-Level Architecture

``` mermaid
flowchart TD
User --> UI["Streamlit UI"]
UI --> Orch["MeetingMind Orchestrator"]
Orch --> SA["SummaryAgent"]
Orch --> TA["TaskAgent"]
Orch --> EA["EmailAgent"]
Orch --> RA["ReviewerAgent"]
SA --> ADK["Google ADK"]
TA --> ADK
EA --> ADK
RA --> ADK
ADK --> Gemini["Gemini"]
Orch --> MCP["Filesystem MCP Client"]
MCP --> FS["Filesystem MCP Server"]
FS --> Files["Local Files"]
```

------------------------------------------------------------------------

# Multi-Agent Workflow

``` mermaid
flowchart LR
Transcript --> Summary --> Tasks --> Email --> Review --> Output
```

------------------------------------------------------------------------

# AI Concepts Demonstrated

  Course Concept       Demonstration
  -------------------- ----------------------------------
  Multi-Agent System   Four collaborating agents
  Google ADK           BaseAgent and specialized agents
  MCP                  Filesystem MCP integration
  Agent Skills         External SKILL.md files
  Security             .env, validation, logging
  Deployability        Streamlit application
  Antigravity          Used during development workflow
  Evaluation           ReviewerAgent

------------------------------------------------------------------------

# Technology Stack

-   Python 3.11+
-   Google Agent Development Kit (ADK)
-   Google Gemini
-   Model Context Protocol (MCP)
-   Streamlit
-   python-dotenv
-   pytest

------------------------------------------------------------------------

# Repository Structure

``` text
src/
├── agents/
├── core/
├── orchestrator/
├── mcp/
├── ui/
└── config.py

tests/
specs/
sample_data/
docs/
```

------------------------------------------------------------------------

# Installation

``` bash
git clone <repository-url>
cd MeetingMind-AI
python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

------------------------------------------------------------------------

# Configuration

Create a `.env` file:

``` env
GEMINI_API_KEY=YOUR_API_KEY
GEMINI_MODEL=gemini-2.5-flash
```

------------------------------------------------------------------------

# Running the Application

``` bash
python -m streamlit run src/ui/streamlit_app.py
```

Run tests:

``` bash
python -m pytest -v
```

------------------------------------------------------------------------

# Example Workflow

1.  Upload meeting transcript
2.  SummaryAgent creates executive summary
3.  TaskAgent extracts actions
4.  EmailAgent drafts follow-up email
5.  ReviewerAgent evaluates outputs
6.  Results displayed and exported

------------------------------------------------------------------------

# Security Features

-   Environment variables for secrets
-   No hardcoded API keys
-   Input validation
-   Structured logging
-   Graceful exception handling
-   Local-first execution

------------------------------------------------------------------------

# Testing

-   Unit Tests
-   Integration Tests
-   End-to-End Validation
-   Manual UI Verification

------------------------------------------------------------------------

# Future Enhancements

-   Calendar integration
-   Email sending
-   Audio transcription
-   Cloud deployment
-   Organizational knowledge (RAG)
-   Advanced analytics dashboard

------------------------------------------------------------------------

# Acknowledgements

Built as the capstone project for the **Google × Kaggle AI Agents:
Intensive Vibe Coding Course** using Google ADK, Gemini, MCP and
Antigravity.

------------------------------------------------------------------------

# License

MIT License.
