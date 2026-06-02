# AI Bug Triage Workflow

This project converts an unstructured QA / regression bug report into a structured JSON object using the OpenAI Responses API with JSON Schema enforcement.

It also:

- validates the structured output
- prepares a Jira-compatible payload
- triggers a Slack-style release blocker alert

---

# Workflow Overview

## Step 1 — Receive Raw Bug Report

The application starts with a messy natural-language bug report:

```python
bug_report = (
    "During regression testing on staging, the login page is not working properly in Chrome..."
)