import os
import json
from common import check_env
from openai import OpenAI

# -----------------------------
# JSON Schema Definition
# -----------------------------

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
        "suggested_next_action": {"type": "string"}
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
    "additionalProperties": False
}


# -----------------------------
# Input Bug Report
# -----------------------------

BUG_REPORT = """
During regression testing on staging, the login page is not working properly in Chrome.

I entered a valid username and password, clicked the Login button, and the page just kept loading.

Expected result: user should land on the dashboard.

Actual result: loading spinner stays forever.

This is blocking our release testing today.

Firefox seems to work fine.
"""


# -----------------------------
# Validate Output
# -----------------------------

def validate_bug(data):
    errors = []

    # steps_to_reproduce must be list
    if not isinstance(data.get("steps_to_reproduce"), list):
        errors.append("steps_to_reproduce must be a list")

    # release_blocker must be boolean
    if not isinstance(data.get("release_blocker"), bool):
        errors.append("release_blocker must be boolean")

    # severity validation
    valid_severity = ["low", "medium", "high", "critical"]

    if data.get("severity") not in valid_severity:
        errors.append(
            "severity must be one of: low, medium, high, critical"
        )

    return errors


# -----------------------------
# Generate Jira Payload
# -----------------------------

def generate_jira_payload(data):

    jira_payload = {
        "summary": data["title"],
        "priority": data["severity"],
        "labels": [
            data["module"],
            data["browser"],
            data["environment"]
        ],
        "description": f"""
Steps:
{chr(10).join(data["steps_to_reproduce"])}

Expected Result:
{data["expected_result"]}

Actual Result:
{data["actual_result"]}

Suggested Next Action:
{data["suggested_next_action"]}
"""
    }

    return jira_payload


# -----------------------------
# Generate Slack Alert
# -----------------------------

def generate_slack_alert(data):

    if not data["release_blocker"]:
        return None

    alert = f"""
🚨 Release Blocker Detected

Bug: {data["title"]}
Module: {data["module"]}
Severity: {data["severity"]}
Environment: {data["environment"]}

Suggested action:
{data["suggested_next_action"]}
"""

    return alert


# -----------------------------
# Main Workflow
# -----------------------------

def main():
    check_env()
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    try:

        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-5.4-mini"),

            instructions="""
You are a bug triage assistant.

Extract structured bug data.

Rules:
- Return valid JSON only
- Do not guess missing information
- Add unclear fields into missing_information
- severity must be one of:
  low, medium, high, critical
- release_blocker must be true or false
""",

            input=BUG_REPORT,

            text={
                "format": {
                    "type": "json_schema",
                    "name": "bug_schema",
                    "schema": BUG_SCHEMA,
                    "strict": True
                }
            }
        )

        # ---------------------------------
        # Parse JSON safely
        # ---------------------------------

        try:
            bug_data = json.loads(response.output_text)

        except json.JSONDecodeError:
            print("❌ AI returned invalid JSON")
            return

        # ---------------------------------
        # Validate Data
        # ---------------------------------

        validation_errors = validate_bug(bug_data)

        if validation_errors:
            print("❌ Validation Errors:")
            for error in validation_errors:
                print("-", error)
            return

        # ---------------------------------
        # Print Structured JSON
        # ---------------------------------

        print("\n✅ STRUCTURED BUG JSON\n")
        print(json.dumps(bug_data, indent=2))

        # ---------------------------------
        # Generate Jira Payload
        # ---------------------------------

        jira_payload = generate_jira_payload(bug_data)

        print("\n✅ JIRA PAYLOAD\n")
        print(json.dumps(jira_payload, indent=2))

        # ---------------------------------
        # Generate Slack Alert
        # ---------------------------------

        slack_alert = generate_slack_alert(bug_data)

        if slack_alert:
            print("\n✅ SLACK ALERT\n")
            print(slack_alert)

        else:
            print("\nNo release blocker detected.")

    except Exception as e:
        print("❌ Workflow failed:")
        print(str(e))


# -----------------------------
# Run App
# -----------------------------

if __name__ == "__main__":
    main()