Overview
----------
This project demonstrates how to convert messy product requirements into structured test cases using an AI workflow.
The workflow extracts the feature name, generates positive/negative/edge test cases, validates them, and produces:

*A structured JSON report
*A test-management-style payload
*A coverage summary

Workflow Steps
---------------
1-Input a messy requirement :-  
Example:

Code
Users should be able to reset their password using an OTP sent to their registered email.
The OTP should expire after 10 minutes.
If the user enters the wrong OTP three times, the account should be temporarily locked.

2-LLM Extraction :-
*The ask_json function sends the requirement to the LLM.
*The LLM is instructed to return only JSON that matches the schema.
*If parsing fails, the code retries once with stricter instructions.

3-Validation :-

*Ensures the JSON matches the schema.
*Checks that:
    test_cases is a list
    Each test case has id, title, type, steps, expected_result, priority
    type is one of: positive, negative, edge
    steps is a list of clear actions

4-Structured Test Report Output :-

*Prints the extracted JSON in a readable format.
*Example: multiple test cases for OTP expiry, wrong attempts, lockout, and edge conditions.

5-Test-Management Payload Generation :-

*Creates a simplified payload with suite name and test cases.
Example:
json
    {
      "suite_name": "Password reset via email OTP with 10-minute expiry and temporary lock after 3 incorrect attempts",
      "test_cases": [
        {
          "title": "Request OTP for password reset - OTP is sent to registered email",
          "priority": "high",
          "steps": ["Enter email", "Submit request", "Check inbox", "Locate OTP"],
          "expected_result": "An OTP is sent to the registered email address."
        }
      ]
    }

6-Coverage Summary Generation :-

*Counts positive, negative, and edge cases.
*Reports missing requirements.
Example:
json
    {
      "positive_cases": 3,
      "negative_cases": 6,
      "edge_cases": 3,
      "missing_requirements_count": 8
    }

Validation Rules
------------------
*Output must be valid JSON
*test_cases → must be a list
*Each test case must include: id, title, type, steps, expected_result, priority
*type → must be one of: positive, negative, edge
*steps → must be a list of clear actions
*missing_requirements → must capture unclear requirements or assumptions


What Could Go Wrong
---------------------
1-Invalid JSON from the LLM

    *The model might return text outside JSON.

    *The code retries once with stricter instructions.

2-Missing required fields

    *If the LLM omits a field, validation will fail.

3-Wrong data types
    *Example: steps returned as a string instead of a list.

4-Unclear requirements

    *If requirements are vague, they appear in missing_requirements.

    *Example: OTP format, lockout duration, boundary behavior at exactly 10 minutes.

5-Ambiguous edge cases

    *Multiple OTP requests, malformed OTP input, or lockout persistence across sessions may need clarification.


Workflow Diagram
------------------
Messy Requirement
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
        +--> Test-Management Payload
        |
        +--> Coverage Summary