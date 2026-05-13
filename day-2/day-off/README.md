# AI Bug Triage Workflow

## Overview

This workflow converts a messy natural-language bug report into structured JSON using the OpenAI API.  
The workflow validates the AI response, detects missing information, and generates downstream system payloads such as Jira-style tickets and Slack-style release blocker alerts.

---

# Input

The workflow accepts a messy bug report written in natural language.

Example:

```text
During regression testing on staging, the login page is not working properly in Chrome.
I entered a valid username and password, clicked the Login button, and the page just kept loading.
Expected result: user should land on the dashboard.
Actual result: loading spinner stays forever.
This is blocking our release testing today.
```

---

# Structured Output

The workflow produces structured JSON in the following format:

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
```

---

# Validation Added

The workflow performs the following validations:

- Ensures valid JSON is returned by the AI
- Checks required fields are present
- Validates `steps_to_reproduce` is a list
- Validates `release_blocker` is a boolean
- Validates severity values:
  - low
  - medium
  - high
  - critical
- Detects missing or unclear information
- Prevents workflow crashes if invalid JSON is returned

---

# System Payloads Generated

## Jira-style Payload

The workflow generates a Jira-ready payload including:

- Summary
- Priority
- Labels
- Description
- Suggested next action

## Slack-style Alert

If `release_blocker` is true, the workflow generates a Slack-style alert message for immediate escalation.

---

# External Systems This Could Connect To

This workflow could integrate with:

- Jira
- Slack
- ServiceNow
- Azure DevOps
- CI/CD pipelines
- QA dashboards

---

# What Could Go Wrong

Possible failure scenarios:

- AI returns invalid JSON
- Missing required fields
- Incorrect severity classification
- Hallucinated information
- Ambiguous bug descriptions
- API failures or rate limits

---

# Future Improvements

Possible improvements for future versions:

- Add schema validation using Pydantic
- Add retry logic for invalid AI responses
- Connect directly to Jira and Slack APIs
- Add logging and monitoring
- Support screenshots and attachments
- Add confidence scoring

---

# How To Run

## Install dependencies

```bash
pip install openai python-dotenv
```

## Add API Key

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

## Run the script

```bash
python structured_bug_workflow.py
```

---

# Files Included

- `structured_bug_workflow.py`
- `README.md`