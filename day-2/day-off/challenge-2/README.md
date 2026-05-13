# AI Test Case Generator Workflow

## Overview

This workflow converts messy product requirements into structured QA test cases using the OpenAI API.  
The workflow validates the AI-generated JSON output, generates positive, negative, and edge test cases, and creates downstream test-management-style payloads along with coverage summaries.

---

# Input

The workflow accepts product requirements written in natural language.

Example:

```text
Users should be able to reset their password using an OTP sent to their registered email.
The OTP should expire after 10 minutes.
If the user enters the wrong OTP three times, the account should be temporarily locked.
```

---

# Structured Output

The workflow produces structured JSON in the following format:

```json
{
  "feature": "Password reset using OTP",
  "test_cases": [
    {
      "id": "TC001",
      "title": "",
      "type": "positive",
      "preconditions": [],
      "steps": [],
      "expected_result": "",
      "priority": "medium"
    }
  ],
  "edge_cases": [],
  "missing_requirements": []
}
```

---

# Validation Added

The workflow performs the following validations:

- Ensures valid JSON is returned by the AI
- Checks required top-level fields
- Validates `test_cases` is a list
- Validates `steps` is a list
- Ensures each test case contains:
  - id
  - title
  - type
  - steps
  - expected_result
  - priority
- Validates test case types:
  - positive
  - negative
  - edge
- Detects unclear or missing requirements
- Prevents workflow crashes if invalid JSON is returned

---

# Test Management Payload

The workflow generates a test-management-style payload including:

- Suite name
- Test case titles
- Priorities
- Steps
- Expected results

Example systems this could integrate with:

- TestRail
- Zephyr
- Jira Xray
- Azure Test Plans

---

# Coverage Summary

The workflow generates a coverage summary including:

- Number of positive test cases
- Number of negative test cases
- Number of edge test cases
- Missing requirements count

---

# External Systems This Could Connect To

This workflow could integrate with:

- TestRail
- Jira
- Zephyr
- Azure DevOps
- CI/CD pipelines
- QA automation frameworks

---

# What Could Go Wrong

Possible failure scenarios:

- AI returns invalid JSON
- Missing required fields
- Incomplete test cases
- Hallucinated assumptions
- Ambiguous requirements
- Incorrect test classifications
- API failures or rate limits

---

# Future Improvements

Possible future enhancements:

- Add schema validation using Pydantic
- Add retry mechanism for invalid JSON
- Integrate directly with test management APIs
- Add support for exporting CSV or Excel
- Add risk-based prioritization
- Add automated test script generation

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
python test_case_generator_workflow.py
```

---

# Files Included

- `test_case_generator_workflow.py`
- `README.md`