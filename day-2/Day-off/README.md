
# README.md: 

##  Workflow

1. **Input:** Receives a raw support message.
2. **AI Processing:** Uses OpenAI to extract key technical details into JSON.
3. **Validation:** Enforces a strict schema to ensure all data (Browser, Steps, etc.) is present.
4. **Payload Generation:** Formats the data into specific templates for Jira and Slack.

---

## Validation Logic

* **Structured Output:** The AI is forbidden from adding extra fields or messy text.
* **No Guessing:** If info is missing, the AI lists it in `missing_information` rather than making it up.
* **Retry Once:** If the first extraction attempt hits an error, the script automatically tries one more time.

##  Potential Failures

* **Missing Key:** The script will fail if the `OPENAI_API_KEY` is not set.
* **Vague Messages:** If the input message is too short (e.g., "It's broken"), the extraction will result in empty fields.
* **Rate Limits:** High-frequency requests may be blocked by the OpenAI API.
=======
## Challenge 1: AI Bug Triage Workflow

### What input does your workflow accept?
A messy, unstructured bug report written in natural language by a QA tester.

### What structured output does it produce?
A validated JSON object with fields:
`title`, `module`, `environment`, `browser`, `severity`, `release_blocker`,
`steps_to_reproduce`, `expected_result`, `actual_result`, `missing_information`, `suggested_next_action`

Also produces:
- A **Jira-style ticket payload** (summary, priority, labels, description)
- A **Slack-style alert message** (only if `release_blocker` is `true`)

### What validation did you add?
- All required fields must be present
- `steps_to_reproduce` must be a list
- `release_blocker` must be a boolean
- `severity` must be one of: `low`, `medium`, `high`, `critical`
- `missing_information` must be a list
- JSON parse errors are caught and reported without crashing the workflow

### What external system could this connect to?
- **Jira REST API** — auto-create tickets
- **Slack Webhooks** — post alerts to QA channel
- **PagerDuty** — trigger on-call alerts for critical blockers
- **TestRail / Xray** — link bugs to test cycles

### What can go wrong with this workflow?
- LLM may return invalid JSON → handled with try/except
- LLM may guess missing fields instead of flagging them
- Severity or boolean fields may be returned as wrong types
- Ambiguous reports may produce inaccurate module/environment detection

### What would you improve next?
- Retry logic if JSON parsing fails (re-prompt LLM to fix its output)
- Confidence scoring per extracted field
- Batch processing of multiple bug reports
- Direct Jira and Slack API integration

---

## Challenge 2: AI Test Case Generator Workflow

### What input does your workflow accept?
A messy product requirement written in plain English by a product manager or BA.

### What structured output does it produce?
A validated JSON object containing:
- `feature` name
- `test_cases` list (positive, negative, edge) with `id`, `title`, `type`,
  `preconditions`, `steps`, `expected_result`, `priority`
- `edge_cases` list
- `missing_requirements` list

Also produces:
- A **test-management-style payload** (suite name + test cases)
- A **coverage summary** (count of positive, negative, edge cases and missing requirements)

### What validation did you add?
- `test_cases` must be a list
- Each test case must have: `id`, `title`, `type`, `steps`, `expected_result`, `priority`
- `type` must be one of: `positive`, `negative`, `edge`
- `steps` must be a list of strings
- JSON parse errors are caught without crashing the workflow

### What external system could this connect to?
- **TestRail API** — auto-import test cases into a test suite
- **Jira Xray** — create test issues from the generated payload
- **Confluence** — publish coverage summaries as documentation
- **GitHub Issues** — create issues for missing requirements

### What can go wrong with this workflow?
- LLM may not generate enough test cases for complex requirements
- Edge cases may overlap with negative cases
- Missing requirements may not be detected if LLM assumes defaults
- Large requirements may exceed token limits
- LLM may return malformed JSON

### What would you improve next?
- Requirement clarification step before generating test cases
- Support multi-feature requirements
- Test case deduplication logic
- BDD-style (Given/When/Then) test case generation option
- Direct TestRail or Xray integration

---

## Workflow Pattern
```
Messy input → LLM extraction → Structured JSON → Validation → System payload → Reviewable output
```
