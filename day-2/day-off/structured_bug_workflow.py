
import json
import os

from common import check_env
from openai import OpenAI

BUG_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "module": {"type": "string"},
        "environment": {"type": "string"},
        "browser": {"type": "string"},

        "severity": {
            "type": "string",
            "enum": ["low", "medium", "high", "critical"]
        },

        "release_blocker": {"type": "boolean"},

        "steps_to_reproduce": {
            "type": "array",
            "items": {"type": "string"}
        },

        "expected_result": {"type": "string"},
        "actual_result": {"type": "string"},

        "missing_information": {
            "type": "array",
            "items": {"type": "string"}
        },

        "suggested_next_action": {"type": "string"},
    },

    "required": [
        "title",
        "module",
        "environment",
        "browser",
        "severity",
        "release_blocker",
        "steps_to_reproduce",
        "expected_result",
        "actual_result",
        "missing_information",
        "suggested_next_action"
    ],

    "additionalProperties": False,
}

BUG_REPORT = input("\nEnter bug report:\n")

def validate_output(data):

    if not isinstance(data.get("steps_to_reproduce"), list):
        print("ERROR: steps_to_reproduce must be a list")
        return False

    if not isinstance(data.get("release_blocker"), bool):
        print("ERROR: release_blocker must be boolean")
        return False

    if data.get("severity") not in ["low", "medium", "high", "critical"]:
        print("ERROR: invalid severity")
        return False

    return True

def generate_jira_payload(data):

    return {
        "summary": data["title"],
        "priority": data["severity"],
        "labels": [
            data["module"].lower(),
            data["browser"].lower(),
            data["environment"].lower()
        ],
        "description": f"""
Steps:
{chr(10).join(data["steps_to_reproduce"])}

Expected Result:
{data["expected_result"]}

Actual Result:
{data["actual_result"]}

Suggested Action:
{data["suggested_next_action"]}
"""
    }


def generate_slack_alert(data):

    if data["release_blocker"]:

        return f"""
    Release Blocker Detected
    
Bug: {data["title"]}
Module: {data["module"]}
Severity: {data["severity"]}
Environment: {data["environment"]}

Suggested action:
Assign to authentication team and collect console logs.
"""

    return None

def main():

    check_env()

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    response = client.responses.create(

        model=os.getenv("OPENAI_MODEL", "gpt-5.4-nano"),

        instructions="""
You are a QA bug triage assistant.

Extract structured JSON from the bug report.

Rules:
- Do NOT guess missing information
- Put unclear details in missing_information
- Ensure severity is one of: low, medium, high, critical
- steps_to_reproduce must be a list
- release_blocker must be boolean
""",

        input=BUG_REPORT,

        text={
            "format": {
                "type": "json_schema",
                "name": "bug_triage",
                "schema": BUG_SCHEMA,
                "strict": True,
            }
        },
    )

    print("\nRAW JSON:")
    print(response.output_text)

    # -----------------------------
    # SAFE JSON PARSING
    # -----------------------------
    try:
        result = json.loads(response.output_text)

    except json.JSONDecodeError:
        print("ERROR: Invalid JSON returned by AI")
        return

    print("\nPARSED OBJECT:")
    print(json.dumps(result, indent=2))

    # -----------------------------
    # VALIDATION
    # -----------------------------
    if not validate_output(result):
        print("Validation failed")
        return

    # -----------------------------
    # JIRA PAYLOAD
    # -----------------------------
    jira_payload = generate_jira_payload(result)

    print("\nJIRA PAYLOAD:")
    print(json.dumps(jira_payload, indent=2))

    # -----------------------------
    # SLACK ALERT (CONDITIONAL)
    # -----------------------------
    slack_alert = generate_slack_alert(result)

    if slack_alert:
        print("\nSLACK ALERT:")
        print(slack_alert)


if __name__ == "__main__":
    main()