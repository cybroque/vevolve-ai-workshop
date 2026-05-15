# QA Test Case Generator Workflow

This workflow automates the transformation of product requirements into structured, high-quality QA test cases using AI. It utilizes Large Language Models (LLMs) to ensure comprehensive coverage including positive, negative, and edge-case scenarios.

## 1. What input does your workflow accept? 
The workflow accepts a **Product Requirement String**. 
* **Example Input:** *"Users should be able to reset their password using an OTP sent to their registered email. The OTP should expire after 10 minutes. If the user enters the wrong OTP three times, the account should be temporarily locked."*

## 2. What structured output does it produce? 
The system produces three distinct levels of structured JSON output:

### A. Comprehensive Test Data
A detailed JSON object containing:
- **Feature Name:** Extracted from the requirement.
- **Test Cases:** An array of objects including `id`, `title`, `type` (positive/negative/edge), `preconditions`, `steps`, `expected_result`, and `priority`.
- **Test Cases:** An array of objects including `id`, `title`, `type` (positive/negative/edge), `preconditions`, `steps`, `expected_result`, and `priority`.
- **Edge Cases:** A list of identified boundary scenarios.
- **Missing Requirements:** A list of ambiguities found in the text that need clarification.

### B. Test Management Payload
A flattened version of the data optimized for importing into test management tools (like Jira, TestRail, or Zephyr), focusing on execution steps and priorities.

### C. Coverage Summary
A high-level metric report providing:
- Count of Positive, Negative, and Edge cases.
- Count of missing requirements to gauge requirement stability.

## 3. What validation did you add?
To ensure the AI output is reliable and parsable, several validation layers were added:
- **Schema Validation:** Uses a JSON Schema with `strict: True` to enforce data types, required fields, and specific enums (e.g., priority must be low/medium/high).
- **Functional Validation (`validate_test_cases`):** A custom Python function that checks for the presence of mandatory fields within the nested test case objects and validates the content of lists (like steps).
- **Retry Mechanism:** If the initial AI response fails validation or is malformed, the workflow automatically attempts a retry to self-correct.

## 4. What external system could this connect to?
This workflow is designed to be a "middle-man" service that could connect to:
- **Jira / Xray / Zephyr:** Automatically create "Test" issue types from the `test_management_payload`.
- **GitHub/GitLab:** Commit generated test cases as Markdown or YAML files directly into a repository.
- **Slack / Microsoft Teams:** Send the `Coverage Summary` to a channel for immediate feedback on requirement clarity.
- **Email Services:** Trigger notifications to Product Managers when `missing_requirements_count` is high.

## 5. What can go wrong with this workflow?
- **Hallucination:** The AI might invent "Expected Results" that weren't intended by the product owner if requirements are too vague.
- **Token Limits:** Extremely long or complex requirement documents might exceed the model's context window.
- **API Reliability:** Dependencies on external LLM providers (like OpenAI) mean the workflow is subject to their uptime and rate limits.
- **Schema Evolution:** If the underlying test management tool changes its requirements, the fixed JSON schema in the code may cause validation failures.

## 6. What would you improve next? 
- **Multi-Requirement Batching:** Allow the workflow to process an entire PRD (Product Requirement Document) rather than single features.
- **Automated Script Generation:** Use the `steps` and `expected_result` to generate boilerplate Playwright or Selenium automation scripts.
- **Semantic Similarity Check:** Prevent duplicate test cases by comparing new generations against existing test suites.
- **Feedback Loop:** Allow QA engineers to "Approve" or "Edit" cases, using that data to fine-tune the prompt instructions for better accuracy.