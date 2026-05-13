"""
Day 2 Challenge - AI Bug Triage Workflow
Three-step workflow:
1. Accept messy bug report input
2. Use LLM to extract structured JSON object (schema enforced)
3. Validate structured JSON against rules
"""

import json
import os
from common import check_env
from openai import OpenAI

# --- Hard-coded bug report ---
bug_report = (
    "During regression testing on staging, the login page is not working properly in Chrome. "
    "I entered a valid username and password, clicked the Login button, and the page just kept loading. "
    "Expected result: user should land on the dashboard. "
    "Actual result: loading spinner stays forever. "
    "This is blocking our release testing today. Firefox seems to work fine."
)

# --- JSON Schema for Bug Report ---
BUG_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "module": {"type": "string"},
        "environment": {"type": "string"},
        "browser": {"type": "string"},
        "severity": {"type": "string", "enum": ["low", "medium", "high"]},
        "release_blocker": {"type": "boolean"},
        "steps_to_reproduce": {"type": "array", "items": {"type": "string"}},
        "expected_result": {"type": "string"},
        "actual_result": {"type": "string"},
        "missing_information": {"type": "array", "items": {"type": "string"}},
        "suggested_next_action": {"type": "string"},
    },
    "required": [
        "title", "module", "environment", "browser", "severity",
        "release_blocker", "steps_to_reproduce",
        "expected_result", "actual_result",
        "missing_information", "suggested_next_action"
    ],
    "additionalProperties": False,
}

def validate_bug(bug):
    errors = []
    if not isinstance(bug.get("steps_to_reproduce"), list):
        errors.append(" steps_to_reproduce must be a list")
    if not isinstance(bug.get("release_blocker"), bool):
        errors.append(" release_blocker must be a boolean")
    if bug.get("severity") not in ["low", "medium", "high"]:
        errors.append(" severity must be one of: low, medium, high")
    return errors

def main():
    check_env()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # --- Step 1: Accept messy bug report ---
    #print("Enter messy bug report (type 'exit' to quit):")
    #user_input = input("Bug Report: ")
    #if user_input.lower() == "exit":
    #    return

    # --- Step 2: LLM extraction with schema enforcement ---
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5.4-nano"),
        instructions="Extract structured bug triage object from the messy report. Return only valid JSON matching schema.",
        input=bug_report,
        text={
            "format": {
                "type": "json_schema",
                "name": "bug",
                "schema": BUG_SCHEMA,
                "strict": True,
            }
        },
    )

    #print("Raw JSON Output:", response.output_text)

    try:
        structured_bug = json.loads(response.output_text)
    except json.JSONDecodeError:
        print(" Invalid JSON returned by model.")
        return

    # --- Step 3: Validation ---
    validation_errors = validate_bug(structured_bug)
    if validation_errors:
        print("Validation Errors:", validation_errors)
    else:
        print("Structured Bug Object is valid!")
        
    print("Parsed Structured Bug:", json.dumps(structured_bug, indent=2))


    # --- Step 5: Jira Payload ---
    jira_payload = {
        "summary": structured_bug["title"],
        "priority": structured_bug["severity"],
        "labels": [
            structured_bug["module"],
            structured_bug["browser"],
            structured_bug["environment"]
        ],
        "description": (
            f" Steps: {structured_bug['steps_to_reproduce']} "
            f" Expected result: {structured_bug['expected_result']}"
            f" Actual result: {structured_bug['actual_result']}"
            f" Suggested next action: {structured_bug['suggested_next_action']}"
        )
            
    }


    #print("Jira Payload:", json.dumps(jira_payload, indent=2))

    # --- Step 6: Slack Alert ---
    if structured_bug["release_blocker"]:
        slack_alert = f"""
            Release Blocker Detected Bug
            Title: {structured_bug['title']}
            Module: {structured_bug['module']}
            Severity: {structured_bug['severity']}
            Environment: {structured_bug['environment']}
            Suggested action: {structured_bug['suggested_next_action']}
        """
        print(slack_alert)

if __name__ == "__main__":
    main()
