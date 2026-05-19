# AI Bug Triage Workflow

## 🔹 Overview
This project implements an AI-powered bug triage workflow that converts messy bug reports into structured JSON using a strict schema and prepares outputs for downstream systems like Jira and Slack.

The workflow ensures reliability by enforcing schema validation, handling errors, and detecting missing information instead of making assumptions.

---

## 🔹 Input
The workflow accepts a messy bug report written in natural language.

Example:
"During regression testing on staging, the login page is not working properly in Chrome..."

---

## 🔹 Output
The workflow produces:
1. Structured JSON object (validated against schema)
2. Jira-style payload for issue tracking
3. Slack-style alert (only if the bug is a release blocker)

---

## 🔹 Workflow Steps
1. Accept messy bug report as input
2. Send input to LLM with strict JSON schema
3. Extract structured JSON using schema enforcement
4. Retry extraction if the first attempt fails
5. Validate structure using predefined schema
6. Detect missing information explicitly
7. Identify if the issue is a release blocker
8. Generate Jira-style payload
9. Generate Slack-style alert (if release_blocker = true)

---

## 🔹 Schema Validation
The workflow uses a strict JSON schema (`TICKET_SCHEMA`) to ensure:
- All required fields are present
- No additional unexpected fields are included
- Data types are correct (e.g., lists, booleans)

Key validations:
- `steps_to_reproduce` must be a list
- `release_blocker` must be boolean
- All required fields must exist
- JSON must strictly match schema

---

## 🔹 Missing Information Handling
The system detects missing or unclear details instead of guessing.

Examples:
- Console logs not provided
- Browser/OS version missing
- Error message not specified

---

## 🔹 External System Integration

### Jira Payload
The workflow generates a Jira-style payload:
- summary
- priority
- labels (module, browser, environment)
- description (steps, expected, actual, suggested action)

### Slack Alert
If the bug is a release blocker, a Slack-style alert is generated containing:
- Bug title
- Module
- Severity
- Environment
- Suggested action

---

## 🔹 Error Handling
- Retries LLM call if extraction fails
- Prevents crashes due to invalid JSON
- Ensures fallback behavior for robustness

---

## 🔹 What Can Go Wrong
- AI may return incomplete or incorrect data
- Severity classification may be inaccurate
- Missing information may not always be detected
- Network/API failures can interrupt workflow

---

## 🔹 Future Improvements
- Add retry limits and exponential backoff
- Use libraries like Pydantic for stricter validation
- Improve prompt engineering for better accuracy
- Add logging and monitoring
- Integrate directly with Jira and Slack APIs

---

## 🔹 Conclusion
This workflow demonstrates a real-world AI engineering pattern:
- Transforming unstructured input into structured data
- Validating outputs using schema
- Handling errors and missing data
- Integrating with downstream systems

It goes beyond simple AI usage and builds a complete, production-style workflow.