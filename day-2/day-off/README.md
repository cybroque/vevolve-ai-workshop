# AI Bug Triage workflow, validation, and what could go wrong 
# Challenge 1: AI Bug Triage Workflow 
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

# Challenge 2: AI Test Case Generator Workflow

## Overview

This project converts a normal product requirement into structured QA test cases using OpenAI structured outputs.

The workflow:
- takes a messy requirement
- extracts the feature name
- generates positive, negative, and edge test cases
- validates the response
- generates test management style payload
- generates coverage summary

---

## Files

- test_case_generator_workflow.py
- README.md

---

## Workflow Steps

1. User gives a product requirement
2. OpenAI model converts it into structured JSON
3. Validation checks required fields
4. If first extraction fails, retry one more time
5. Generate test management payload
6. Generate coverage summary

---

## Validation Done

The workflow checks:

- JSON format is valid
- test_cases must be a list
- each test case should contain:
  - id
  - title
  - type
  - steps
  - expected_result
  - priority
- type should be:
  - positive
  - negative
  - edge
- steps must be a list
- missing_requirements must be a list

---

## Coverage Summary

The workflow generates:
- positive test case count
- negative test case count
- edge test case count
- missing requirement count

---

## What Could Go Wrong

- Some test cases may miss required fields
- AI may misunderstand the requirement
- API/network failures can happen

---

## Future Improvements

- Add database storage
- Connect with real test management tools
- Add logging and monitoring
- Improve retry and validation handling