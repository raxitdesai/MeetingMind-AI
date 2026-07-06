\# MeetingMind AI



\*\*Version:\*\* 1.0  

\*\*Project Type:\*\* Multi-Agent AI Application  

\*\*Track:\*\* Concierge Agents  

\*\*Capstone:\*\* Kaggle AI Agents: Intensive Vibe Coding with Google



\---



\# 1. Executive Summary



MeetingMind AI is a lightweight Multi-Agent AI application that transforms unstructured meeting transcripts into structured meeting intelligence.



The application is designed to demonstrate modern AI Agent Engineering concepts taught in Google's AI Agents: Intensive Vibe Coding course while remaining intentionally simple and easy to understand.



MeetingMind AI uses a team of specialized AI agents that collaborate to:



\- Generate concise meeting summaries

\- Extract action items

\- Draft professional follow-up emails

\- Evaluate the quality of generated outputs



The application demonstrates the following concepts:



\- Google Agent Development Kit (ADK)

\- Multi-Agent Orchestration

\- Agent Skills

\- Model Context Protocol (MCP)

\- Human-in-the-loop approval

\- Evaluation

\- Spec-Driven Development



The project is intentionally limited in scope to maximize clarity, maintainability, and educational value.



The final application will run locally using Streamlit and Gemini models without requiring cloud deployment or external integrations.



\---



\# 2. Business Problem



Many professionals spend considerable time after meetings manually preparing summaries, documenting decisions, extracting action items, and drafting follow-up emails.



These repetitive activities reduce productivity and often lead to missed tasks, inconsistent documentation, and communication delays.



Although large enterprise meeting assistants exist, they are often complex, expensive, and tightly integrated with enterprise ecosystems.



MeetingMind AI demonstrates that a small team of specialized AI agents can automate the majority of post-meeting activities using modern AI engineering techniques.



The project serves as an educational reference implementation for building trustworthy AI agents using Google's ADK ecosystem.



\---



\# 3. Project Goals



The project has four primary goals.



\## Goal 1



Demonstrate a complete Multi-Agent workflow using Google ADK.



\## Goal 2



Show how reusable Agent Skills improve maintainability.



\## Goal 3



Demonstrate secure interaction with local files using Filesystem MCP.



\## Goal 4



Provide a simple, educational example of AI Agent Engineering suitable for beginners.



Success will be measured by successful execution of the end-to-end workflow rather than production-scale performance.



\---



\# 4. Success Metrics



The project will be considered successful when:



\- Users can upload a meeting transcript.

\- The Summary Agent generates a structured summary.

\- The Task Agent extracts action items.

\- The Email Agent drafts a professional follow-up email.

\- The Reviewer Agent evaluates the generated outputs.

\- Outputs are saved locally using the Filesystem MCP server.

\- All functionality is available through a simple Streamlit interface.

\- No external actions are performed automatically.

\- The project demonstrates the key concepts taught in the Google AI Agents course.



\---



\# 5. Scope



\## In Scope



\- Upload meeting transcript (.txt)

\- Generate structured meeting summary

\- Extract action items

\- Draft follow-up email

\- Evaluate generated outputs

\- Save outputs locally

\- Human approval before any external action

\- Local Streamlit application

\- Google ADK Multi-Agent architecture

\- Filesystem MCP integration



\## Out of Scope



\- Authentication

\- User accounts

\- Database

\- Cloud deployment

\- Gmail integration

\- Google Calendar integration

\- Slack or Teams integration

\- Voice transcription

\- OCR

\- Retrieval-Augmented Generation (RAG)

\- Vector databases

\- Multi-user collaboration



\---



\# 6. User Persona



\## Primary User



Knowledge workers who frequently participate in meetings and want to reduce the manual effort required to prepare meeting summaries and follow-up documentation.



Typical users include:



\- Project Managers

\- Product Managers

\- Team Leads

\- Software Engineers

\- Business Analysts

\- Consultants

\- Students



\---



\# 7. User Journey



1\. Launch MeetingMind AI.

2\. Upload a meeting transcript.

3\. Click \*\*Analyze\*\*.

4\. Summary Agent creates the meeting summary.

5\. Task Agent extracts action items.

6\. Email Agent drafts the follow-up email.

7\. Reviewer Agent evaluates the outputs.

8\. User reviews the generated content.

9\. User approves and exports the results.



\---



\# 8. Functional Requirements



| ID | Requirement |

|----|-------------|

| FR-01 | Upload a meeting transcript |

| FR-02 | Generate a structured meeting summary |

| FR-03 | Extract action items |

| FR-04 | Draft a follow-up email |

| FR-05 | Evaluate generated outputs |

| FR-06 | Save outputs using Filesystem MCP |

| FR-07 | Display outputs in Streamlit |

| FR-08 | Maintain an audit log |

| FR-09 | Require user approval before external actions |



\---



\# 9. Non-Functional Requirements



\## Performance



\- Average response time under 30 seconds.



\## Reliability



\- Gracefully handle invalid or empty transcripts.



\## Maintainability



\- Modular architecture.

\- Independent agents.

\- Reusable skills.



\## Security



\- Human approval required.

\- No automatic external communication.

\- Environment variables for secrets.

\- Local-only filesystem access.



\## Usability



\- Single-page Streamlit application.

\- Minimal user interaction.

\- Clear and readable outputs.



\---



\# 10. Multi-Agent Architecture



MeetingMind AI consists of four specialized agents.



\## SummaryAgent



Produces a structured meeting summary.



\## TaskAgent



Extracts structured action items.



\## EmailAgent



Creates a professional follow-up email.



\## ReviewerAgent



Evaluates outputs generated by the other agents.



The agents execute sequentially.



```

Transcript

&#x20;   ↓

SummaryAgent

&#x20;   ↓

TaskAgent

&#x20;   ↓

EmailAgent

&#x20;   ↓

ReviewerAgent

```



\---



\# 11. Agent Responsibilities



| Agent | Responsibility |

|--------|----------------|

| SummaryAgent | Meeting summary |

| TaskAgent | Action items |

| EmailAgent | Follow-up email |

| ReviewerAgent | Quality evaluation |



Each agent has exactly one responsibility.



\---



\# 12. MCP Requirements



MeetingMind AI uses the Filesystem MCP server.



The MCP server is responsible for:



\- Reading uploaded transcripts

\- Saving generated summaries

\- Saving extracted tasks

\- Saving email drafts

\- Saving evaluation reports



The MCP server must never:



\- Delete files

\- Modify files outside the project directory

\- Execute operating system commands



\---



\# 13. Agent Skills



Each AI agent uses a reusable Skill.



| Skill | Used By |

|-------|----------|

| Meeting Summarization | SummaryAgent |

| Task Extraction | TaskAgent |

| Email Writing | EmailAgent |

| Output Review | ReviewerAgent |



Skills define the behavior of each agent independently from the application code.



\---



\# 14. Security



MeetingMind AI follows a Human-in-the-Loop model.



Rules:



\- Never send emails automatically.

\- Never perform external actions.

\- Never expose API keys.

\- Limit filesystem access to the project directory.

\- Log user approval events.

\- Sanitize generated output before displaying it.



\---



\# 15. Evaluation



The ReviewerAgent evaluates:



\- Summary quality

\- Task completeness

\- Email quality

\- Consistency across outputs

\- Missing information

\- Potential hallucinations



Output:



```json

{

&#x20; "overall\_score": 95,

&#x20; "summary\_score": 96,

&#x20; "task\_score": 93,

&#x20; "email\_score": 97,

&#x20; "issues": \[],

&#x20; "suggestions": \[]

}

```



\---



\# 16. User Interface



The application uses a single Streamlit page.



Main components:



\- Upload Transcript

\- Analyze Button

\- Meeting Summary

\- Action Items

\- Follow-up Email

\- Evaluation Report

\- Audit Log



The interface should remain intentionally simple.



\---



\# 17. Folder Structure



```

MeetingMind-AI/



README.md



specs/

&#x20;   product\_spec.md



.agent/

&#x20;   AGENTS.md



.agent/skills/

&#x20;   summarize/

&#x20;   extract\_tasks/

&#x20;   email\_writer/

&#x20;   reviewer/



src/

&#x20;   agents/

&#x20;   mcp/

&#x20;   ui/

&#x20;   security/

&#x20;   evaluation/



sample\_data/



output/



tests/

```



\---



\# 18. Data Contracts



\## Summary Output



```json

{

&#x20; "meeting\_title": "",

&#x20; "meeting\_date": "",

&#x20; "participants": \[],

&#x20; "summary": "",

&#x20; "decisions": \[],

&#x20; "risks": \[],

&#x20; "next\_steps": \[]

}

```



\## Task Output



```json

\[

&#x20; {

&#x20;   "task": "",

&#x20;   "owner": "",

&#x20;   "deadline": "",

&#x20;   "priority": ""

&#x20; }

]

```



\## Email Output



```json

{

&#x20; "subject": "",

&#x20; "body": ""

}

```



\## Review Output



```json

{

&#x20; "overall\_score": 95,

&#x20; "summary\_score": 95,

&#x20; "task\_score": 95,

&#x20; "email\_score": 95,

&#x20; "issues": \[],

&#x20; "suggestions": \[]

}

```



\---



\# 19. Acceptance Criteria



The project is complete when:



\- Transcript upload works.

\- All four agents execute successfully.

\- Outputs conform to the defined JSON contracts.

\- Files are saved using the Filesystem MCP server.

\- ReviewerAgent generates evaluation scores.

\- Human approval is demonstrated.

\- Streamlit UI works correctly.

\- Unit tests pass.

\- Documentation is complete.



\---



\# 20. Future Enhancements



Potential future improvements include:



\- Google Calendar integration

\- Gmail integration

\- Meeting audio transcription

\- PDF export

\- Slack notifications

\- RAG over previous meetings

\- Cloud deployment

\- Authentication

\- Multi-user support



These enhancements are intentionally excluded from the current capstone project.

