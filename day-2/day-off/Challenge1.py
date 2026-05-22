"""
Simple AI Bug Report Workflow
Day 2, Session 4: Structured Outputs Part A

Learning Objective:
Validate structured AI output using Python schema.
"""

import json
import os

from openai import OpenAI


# JSON Schema
BUG_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "module": {"type": "string"},
        "environment": {"type": "string"},
        "browser": {"type": "string"},
        "severity": {"type": "string"},
        "release_blocker": {"type": "boolean"},
        "steps_to_reproduce": {"type": "array"},
        "expected_result": {"type": "string"},
        "actual_result": {"type": "string"},
        "missing_information": {"type": "array"},
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


def validate_schema(data):
    """Check required fields."""

    required = [
        "title",
        "module",
        "environment",
        "browser",
        "severity",
        "release_blocker",
    ]

    for key in required:
        if key not in data:
            return False, f"Missing field: {key}"

    return True, "Valid"


def main():

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    bug_report = """
    During regression testing on staging, login page is not working in Chrome.
    After clicking Login, loading spinner keeps spinning forever.

    Expected result: User should go to dashboard.
    Actual result: Page keeps loading.

    This is blocking release testing today.
    """

    response = client.responses.create(
        model="gpt-4o-mini",

        instructions="""
        Extract bug details into structured JSON.
        Do not guess missing information.
        """,

        input=bug_report,

        text={
            "format": {
                "type": "json_schema",
                "name": "bug_report",
                "schema": BUG_SCHEMA,
                "strict": True,
            }
        },
    )

    # Convert response to JSON
    data = json.loads(response.output_text)

    # Validate JSON
    valid, message = validate_schema(data)

    print("Validation:", message)

    # Print structured JSON
    print("\nStructured JSON:")
    print(json.dumps(data, indent=2))

    # Jira payload
    jira_payload = {
        "summary": data["title"],
        "priority": data["severity"],
        "labels": [
            data["module"],
            data["browser"],
            data["environment"]
        ]
    }

    print("\nJira Payload:")
    print(json.dumps(jira_payload, indent=2))

    # Slack alert
    if data["release_blocker"]:

        print("\nSlack Alert:")
        print(f"""
Release Blocker Detected

Bug: {data['title']}
Severity: {data['severity']}
Environment: {data['environment']}
""")


if __name__ == "__main__":
    main()