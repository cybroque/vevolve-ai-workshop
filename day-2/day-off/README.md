# AI Bug Triage workflow, validation, and what could go wrong 

## Overview

This project converts messy QA bug reports into structured JSON using OpenAI structured outputs.

The workflow:
- takes a normal bug report
- extracts important details using AI
- validates the response
- generates Jira style payload
- generates Slack alert if it is a release blocker

---

## Files

- structured_bug_workflow.py
- README.md

---

## Workflow Steps

1. User gives a messy bug report
2. OpenAI model converts it into structured JSON
3. Validation checks required fields
4. If first extraction fails, retry one more time
5. Generate Jira payload
6. Generate Slack alert if release_blocker is true

---

## Validation Done

The workflow checks:

- JSON format is valid
- severity must be:
  - low
  - medium
  - high
  - critical
- release_blocker must be boolean
- steps_to_reproduce must be a list
- missing_information must be a list
- all required fields should exist

---

## What Could Go Wrong

- Invalid API key or missing environment variables can cause failures
- Network/API issues may interrupt the workflow

---

## Future Improvements

- Add logging and monitoring
- Connect directly with Jira and Slack APIs