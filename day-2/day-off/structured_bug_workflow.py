"""Structured output pattern: extract, validate, and retry once."""

import json
import os
import sys
from pathlib import Path

from common import check_env
from openai import OpenAI

sys.path.append(str(Path(__file__).resolve().parents[2]))

BUG_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "module": {"type": "string"},
        "environment": {"type": "string"},
        "browser": {"type": "string"},
        "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
        "release_blocker": {"type": "boolean"},
        "steps_to_reproduce": {"type": "array", "items": {"type": "string"}},
        "expected_result": {"type": "string"},
        "actual_result": {"type": "string"},
        "missing_information": {"type": "array", "items": {"type": "string"}},
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
        "suggested_next_action",
    ],
    "additionalProperties": False,
}


def ask_json(prompt, schema, *, name="bug_report"):
    check_env()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    try:
        response = client.responses.create(
            model="gpt-5.4-nano",
            instructions="Return only JSON that matches the provided schema.",
            input=prompt,
            text={
                "format": {
                    "type": "json_schema",
                    "name": name,
                    "schema": schema,
                    "strict": True,
                }
            },
        )
        return json.loads(response.output_text)
    except Exception:
        # retry once
        response = client.responses.create(
            model="gpt-5.4-nano",
            instructions="Return valid JSON only. No text outside JSON.",
            input=prompt,
            text={
                "format": {
                    "type": "json_schema",
                    "name": name,
                    "schema": schema,
                    "strict": True,
                }
            },
        )
        return json.loads(response.output_text)


def main():
    message = """
    During regression testing on staging, the login page is not working properly in Chrome.
    I entered a valid username and password, clicked the Login button, and the page just kept loading.
    Expected result: user should land on the dashboard.
    Actual result: loading spinner stays forever.
    This is blocking our release testing today. Firefox seems to work fine.
    """

    prompt = f"""
    Extract this bug report into structured JSON.
    Detect missing information instead of guessing blindly.
    Decide if this is a release blocker.
    Message:
    {message}
    """

    try:
        bug = ask_json(prompt, BUG_SCHEMA)
    except Exception as exc:
        print(f"Extraction failed: {exc}")
        return

    # Basic validation
    errors = []
    if bug.get("severity") not in ["low", "medium", "high", "critical"]:
        errors.append("Invalid severity")
    if not isinstance(bug.get("steps_to_reproduce"), list):
        errors.append("steps_to_reproduce must be a list")
    if not isinstance(bug.get("release_blocker"), bool):
        errors.append("release_blocker must be a boolean")
    if errors:
        print("Validation errors:", errors)
        return

    print("Structured Bug Report:")
    print(json.dumps(bug, indent=2))

    # Jira payload
    jira_payload = {
        "summary": bug["title"],
        "priority": bug["severity"],
        "labels": [bug["module"], bug["browser"], bug["environment"]],
        "description": (
            f"Steps: {bug['steps_to_reproduce']}\n"
            f"Expected: {bug['expected_result']}\n"
            f"Actual: {bug['actual_result']}\n"
            f"Next Action: {bug['suggested_next_action']}"
        ),
    }
    print("\nJira Payload:")
    print(json.dumps(jira_payload, indent=2))

    # Slack alert
    if bug["release_blocker"]:
        print("\nSlack Alert:")
        print(f"""
Release Blocker Detected
Bug: {bug['title']}
Module: {bug['module']}
Severity: {bug['severity']}
Environment: {bug['environment']}
Suggested action:
{bug['suggested_next_action']}
""")

if __name__ == "__main__":
    main()
