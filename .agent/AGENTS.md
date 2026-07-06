# MeetingMind AI - AGENTS.md

## Project Purpose

MeetingMind AI is a lightweight Multi-Agent AI application developed as
part of the **Kaggle AI Agents: Intensive Vibe Coding Capstone
Project**.

The application demonstrates modern AI Agent Engineering concepts using:

- Google Agent Development Kit (ADK)
- Gemini Models
- Antigravity IDE
- Model Context Protocol (MCP)
- Agent Skills
- Spec-Driven Development (SDD)
- Security Guardrails
- Evaluation

The objective is to build a **simple, modular, production-inspired AI
application** rather than an enterprise-scale solution.

------------------------------------------------------------------------

# Project Philosophy

This project intentionally favors:

- Simplicity
- Readability
- Small reusable components
- Explicit code
- Easy debugging
- Clear agent responsibilities

Avoid unnecessary abstraction.

Avoid unnecessary frameworks.

Prefer code that is easy to understand over code that is clever.

Every generated component should be easy for a beginner to understand.

------------------------------------------------------------------------

# Spec-Driven Development

The specification is the single source of truth.

Before writing code:

1.  Read the project specification.
2.  Resolve ambiguities.
3.  Generate architecture.
4.  Wait for approval before implementing major changes.

Never invent features that are not present in the specification.

------------------------------------------------------------------------

# Overall Architecture

MeetingMind AI consists of four AI agents and one MCP Tool.

    User
        │
        ▼
    Summary Agent
        │
        ▼
    Task Extraction Agent
        │
        ▼
    Email Draft Agent
        │
        ▼
    Reviewer Agent
        │
        ▼
    Filesystem MCP Tool
        │
        ▼
    Streamlit UI

------------------------------------------------------------------------

# Agent Responsibilities

## Summary Agent

Input

Meeting transcript

Output

Structured meeting summary.

Responsibilities

- Meeting objective
- Key discussion
- Decisions
- Risks
- Next steps

------------------------------------------------------------------------

## Task Extraction Agent

Input

Meeting transcript

Output

Structured action items.

Responsibilities

- Task
- Owner
- Due date
- Priority

------------------------------------------------------------------------

## Email Draft Agent

Input

Summary

Action Items

Output

Professional follow-up email.

------------------------------------------------------------------------

## Reviewer Agent

Input

Outputs from all agents.

Responsibilities

- Quality evaluation
- Completeness
- Missing information
- Suggestions
- Confidence score

------------------------------------------------------------------------

# ADK Orchestration Principles

Each agent must have a single responsibility.

Prefer sequential orchestration.

Avoid nested agent loops.

Pass structured outputs between agents.

Each agent should be independently testable.

Avoid hidden side effects.

Do not allow agents to directly modify application state.

------------------------------------------------------------------------

# Output Contracts

## Summary Agent

Returns

    {
      "meeting_title": "",
      "summary": "",
      "decisions": [],
      "risks": [],
      "next_steps": []
    }

------------------------------------------------------------------------

## Task Agent

Returns

    [
      {
        "task": "",
        "owner": "",
        "deadline": "",
        "priority": ""
      }
    ]

------------------------------------------------------------------------

## Email Agent

Returns

    {
      "subject": "",
      "body": ""
    }

------------------------------------------------------------------------

## Reviewer Agent

Returns

    {
      "overall_score": 95,
      "summary_score": 96,
      "task_score": 92,
      "email_score": 97,
      "issues": [],
      "suggestions": []
    }

------------------------------------------------------------------------

# MCP Guidelines

Use the Filesystem MCP server.

Filesystem MCP may:

- Read meeting transcripts
- Save summaries
- Save action items
- Save email drafts
- Read generated outputs

Filesystem MCP must NOT:

- Delete files
- Access files outside the project
- Modify operating system files
- Execute arbitrary commands

------------------------------------------------------------------------

# Agent Skills

Each reusable capability must be implemented as a Skill.

Skills should remain independent of business logic.

Expected skills include:

- Meeting Summarization
- Task Extraction
- Email Writing
- Output Review

Each skill should contain:

- Purpose
- Trigger
- Inputs
- Outputs
- Constraints
- Examples

------------------------------------------------------------------------

# Security Guidelines

Never perform external actions automatically.

Always require human approval before:

- Sending emails
- Exporting data
- Calling external services

Never expose:

- API keys
- Environment variables
- Internal paths

Limit MCP access to the project directory.

Sanitize all generated output before displaying it.

------------------------------------------------------------------------

# Prompt Engineering Guidelines

Prompts should:

- Be deterministic
- Be concise
- Produce structured outputs
- Avoid unnecessary verbosity
- Minimize hallucinations

Prefer JSON or Pydantic-compatible outputs whenever possible.

Avoid free-form text unless explicitly required.

------------------------------------------------------------------------

# Python Coding Standards

Follow PEP 8.

Use:

- Type hints
- Google Style Docstrings
- Small functions
- Clear variable names

Prefer composition over inheritance.

Avoid functions longer than approximately 40 lines whenever practical.

------------------------------------------------------------------------

# Logging

Log:

- Agent execution
- Tool invocation
- Evaluation results
- Errors
- User approval events

Do not log:

- API keys
- Secrets
- Personal information

------------------------------------------------------------------------

# Error Handling

Handle failures gracefully.

Catch:

- Gemini API failures
- MCP failures
- Missing files
- Invalid transcripts

Return meaningful error messages.

------------------------------------------------------------------------

# Evaluation Principles

Reviewer Agent evaluates:

- Summary completeness
- Missing action items
- Missing owners
- Missing deadlines
- Email quality
- Consistency between outputs

Return:

- Overall score
- Individual scores
- Suggestions
- Confidence level

------------------------------------------------------------------------

# Testing Guidelines

Write:

- Unit Tests
- Integration Tests
- End-to-End Tests

Mock:

- Gemini API
- MCP calls

Every agent should have at least one positive and one negative test
case.

------------------------------------------------------------------------

# Naming Conventions

Agent classes

- SummaryAgent
- TaskAgent
- EmailAgent
- ReviewerAgent

Skill folders

- summarize
- extract_tasks
- email_writer
- reviewer

Use descriptive names throughout the project.

------------------------------------------------------------------------

# Documentation Standards

Every module should include:

- Purpose
- Inputs
- Outputs
- Dependencies

Maintain:

- README
- Architecture Diagram
- Project Specification

Keep documentation synchronized with implementation.

------------------------------------------------------------------------

# Out of Scope

Do NOT add:

- Authentication
- Database
- Cloud Deployment
- Gmail Integration
- Calendar Integration
- Slack Integration
- Voice Transcription
- RAG
- Vector Database
- Multi-user Support
- Background Workers

This project intentionally remains simple.

------------------------------------------------------------------------

# Development Workflow

Follow this sequence:

1.  Read Specification
2.  Review Requirements
3.  Generate Small Components
4.  Review Code
5.  Run Tests
6.  Commit Changes

Never generate the entire application in one step.

------------------------------------------------------------------------

# Review Checklist

Before completing any feature verify:

- Specification followed
- Small readable code
- Structured outputs
- Security respected
- Human approval preserved
- Logging added
- Tests updated
- Documentation updated

If unsure, stop and ask for clarification instead of making assumptions.
