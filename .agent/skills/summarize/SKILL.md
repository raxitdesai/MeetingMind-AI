---
name: Meeting Summarization
description: Summarizes meeting transcripts into structured JSON summaries containing objective, key discussions, decisions, risks, and next steps.
---

# Meeting Summarization Skill

## Purpose
This skill enables an AI agent to analyze a raw meeting transcript and produce a highly structured, concise, and accurate JSON summary. It captures the essential context of the meeting including the title, main summary, key decisions made, identified risks, and next steps.

## Trigger
- When a raw meeting transcript (text format) is provided.
- When a user asks for a summary, key decisions, or general overview of a meeting transcript.

## Inputs
- `transcript` (string): The raw text transcript of the meeting, typically containing speaker names and timestamps.

## Outputs
A JSON object adhering to the following schema:
```json
{
  "meeting_title": "String - Descriptive title of the meeting, or 'Not mentioned' if unclear",
  "summary": "String - A concise, high-level summary of the meeting objective and main discussion points",
  "decisions": [
    "String - Key decisions made during the meeting"
  ],
  "risks": [
    "String - Identified risks, roadblocks, or concerns raised"
  ],
  "next_steps": [
    "String - Next steps or action items outlined"
  ]
}
```

## Constraints
1. **No Hallucinations**: Every piece of information in the output must be directly supported by the transcript.
2. **Handle Missing Information**: If any field (e.g., decisions, risks, next_steps) is not discussed or present in the transcript, the array must contain a single string: `"Not mentioned"`. If the title or summary cannot be determined, set them to `"Not mentioned"`.
3. **Strict JSON Format**: The output must be valid JSON, containing only the specified keys.
4. **Conciseness**: Summaries and list items must be clear, actionable, and free of fluff.
5. **No External Actions**: Do not assume external events, schedule invites, or send emails.

## Best Practices
- Focus on key outcomes and align next steps with mentioned owners if present.
- Identify implicit risks (e.g., missed deadlines, resource constraints, technical challenges) mentioned by speakers.
- Distinguish between discussion/options and final decisions. Only list final decisions in `decisions`.

## Example Input
```text
Speaker A (00:01): Thanks for joining the sync. Today we need to decide on our database migration plan. We are currently split between Postgres and MongoDB.
Speaker B (01:15): MongoDB offers flexibility, but Postgres gives us strong ACID compliance which is critical for our transactional data. If we go with Postgres, we might need to train the team on SQL, which could delay the launch by a week.
Speaker A (02:30): That's a valid risk, but the transactional integrity is non-negotiable. Let's decide on PostgreSQL.
Speaker B (03:00): Agreed. Let's do it. I'll spin up the dev instance by Friday.
Speaker A (03:45): Great. I'll draft the schema design document and share it for review next Monday. Let's end the meeting here.
```

## Example Output
```json
{
  "meeting_title": "Database Migration Sync",
  "summary": "The team met to decide on the database migration plan, comparing PostgreSQL and MongoDB. PostgreSQL was chosen to ensure strong ACID compliance for transactional data.",
  "decisions": [
    "Adopted PostgreSQL for the database migration due to ACID compliance requirements."
  ],
  "risks": [
    "Potential team training requirements for SQL could delay the launch by one week."
  ],
  "next_steps": [
    "Spin up the PostgreSQL dev instance by Friday (Owner: Speaker B).",
    "Draft the schema design document and share it for review by next Monday (Owner: Speaker A)."
  ]
}
```

## Prompt Template
```text
You are a Summary Agent. Analyze the meeting transcript provided below and extract a structured summary.

Constraints:
- Respond ONLY with a valid JSON object matching the schema below. Do not include markdown code block formatting (like ```json ... ```) or any preamble/postamble.
- Keep the summary and list items extremely concise and factual.
- Do NOT hallucinate.
- If decisions, risks, or next steps are not mentioned in the transcript, populate the respective array with a single element: "Not mentioned".
- If the meeting title is not mentioned or cannot be inferred, set the "meeting_title" to "Not mentioned".

Output Schema:
{
  "meeting_title": "Descriptive title of the meeting or 'Not mentioned'",
  "summary": "Concise summary of the meeting objective and key discussions",
  "decisions": ["Decision 1", "Decision 2"],
  "risks": ["Risk 1", "Risk 2"],
  "next_steps": ["Next step 1", "Next step 2"]
}

Meeting Transcript:
{transcript}
```
