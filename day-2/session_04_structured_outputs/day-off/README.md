# AI Bug Triage Workflow
This workflow converts messy natural-language QA bug reports into:

1. Structured JSON
2. Validated bug objects
3. Jira-style payloads
4. Slack alerts for release blockers

The system is designed to be resilient against incomplete or invalid AI responses.

# Workflow Steps
1. Input

The workflow accepts raw bug reports written in free-form natural language.

Example:

"Login page keeps loading forever in Chrome during staging regression testing."

---
2. AI Extraction

The LLM extracts a structured JSON object using a predefined schema.

Expected schema:

```json
{
  "title": "",
  "module": "",
  "environment": "",
  "browser": "",
  "severity": "",
  "release_blocker": false,
  "steps_to_reproduce": [],
  "expected_result": "",
  "actual_result": "",
  "missing_information": [],
  "suggested_next_action": ""
}

3. Validation

The workflow validates:

Required fields exist
steps_to_reproduce is a list
release_blocker is a boolean
severity is one of:
low
medium
high
critical
missing_information is a list

If validation fails:

Defaults are applied safely
Errors are added to missing_information
The system does not crash

4. Missing Information Detection

The workflow intentionally avoids hallucinating missing details.

Examples of detected missing info:

Chrome version
Operating system
Console logs
Network traces

5. Release Blocker Detection

If:

bug blocks testing/release
or severity is high/critical

6. Jira Payload Generation

The workflow creates a Jira-compatible payload:

7.error handling


POSSIBLE FAILURES:-
=================

1.hallicunate values
2.incomplete report
3.invalid json 