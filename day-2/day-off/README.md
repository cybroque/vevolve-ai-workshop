Overview
----------
This project demonstrates a structured output pattern using an LLM (Large Language Model). The workflow takes a messy bug report as input, extracts structured information in JSON format, validates it, and then generates:

* A Jira‑style payload for issue tracking
* A Slack‑style alert if the bug is a release blocker

Workflow Steps
----------------
1-Input a messy bug report :-

Example:
During regression testing on staging, the login page is not working properly in Chrome.
I entered a valid username and password, clicked the Login button, and the page just kept loading.
Expected result: user should land on the dashboard.
Actual result: loading spinner stays forever.
This is blocking our release testing today. Firefox seems to work fine.

2-LLM Extraction :-

* The ask_json function sends the bug report to the LLM.
* The LLM is instructed to return only JSON that matches the schema.
* If parsing fails, the code retries once with stricter instructions.

3-Validation :-

* Ensures the JSON matches the schema.
* Checks that:
    severity is one of: low, medium, high, critical
    steps_to_reproduce is a list
    release_blocker is a boolean
* If validation fails, errors are printed and the workflow stops.

4-Structured Bug Report Output :-

* Prints the extracted JSON in a readable format.

5-Jira Payload Generation :-

* Creates a simplified payload with:
json
    {
      "summary": "Login page stuck after valid login on Chrome",
      "priority": "high",
      "labels": ["authentication", "Chrome", "staging"],
      "description": "Steps, expected result, actual result, and suggested next action"
    }

6-Slack Alert Generation :-

* If release_blocker is true, prints:
Code
    Release Blocker Detected
    Bug: Login page stuck after valid login on Chrome
    Module: authentication
    Severity: high
    Environment: staging
    Suggested action:
    Assign to authentication team and collect console logs.

Validation Rules
-------------------
* Output must be valid JSON
* steps_to_reproduce → must be a list
* release_blocker → must be a boolean (true or false)
* severity → must be one of: low, medium, high, critical
* missing_information → must list unclear or missing details

What Could Go Wrong
---------------------
1-Invalid JSON from the LLM
    The model might return text outside JSON.
    The code retries once with stricter instructions.
2-Missing required fields
    If the LLM omits a field, validation will fail.
3-Wrong data types
    Example: release_blocker returned as "true" (string) instead of true (boolean).
4-Severity mismatch
    If severity is not one of the allowed values, validation fails.
5-Incomplete bug report
    If important details (like environment or steps) are missing, they appear in missing_information.


Workflow Diagram 
-------------------
Messy Bug Report
        |
        v
   ask_json() ----> Retry once if invalid JSON
        |
        v
   Validation ----> Errors? Stop
        |
        v
 Structured JSON
        |
        |--> Jira Payload
        |
        |--> Slack Alert (only if release_blocker = true)