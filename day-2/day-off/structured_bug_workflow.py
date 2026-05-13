import json
import os
import sys
from pathlib import Path

from common import check_env
from openai import OpenAI

sys.path.append(str(Path(__file__).resolve().parents[2]))

TICKET_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "module": {"type": "string"},
        "environment": {"type": "string"},
        "browser": {"type": "string"},
        "severity": {"type": "string"},
        "release_blocker": {"type": "boolean"},
        "steps_to_reproduce": {"type": "array", "items": {"type": "string"}},
        "expected_result": {"type": "string"},
        "actual_result": {"type": "string"},
        "missing_information": {"type": "array", "items": {"type": "string"}},
        "suggested_next_action": {"type": "string"},
    },
    "required": [
        "title", "module", "environment", "browser", "severity",
        "release_blocker", "steps_to_reproduce", "expected_result",
        "actual_result", "missing_information", "suggested_next_action"
    ],
    "additionalProperties": False,
}


def ask_json(prompt, schema, *, name="support_ticket"):
    check_env()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Using chat.completions as it is the standard for structured JSON output
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "Return only JSON that matches the provided schema. Detect missing info."},
            {"role": "user", "content": prompt}
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": name,
                "schema": schema,
                "strict": True
            }
        }
    )
    return json.loads(response.choices[0].message.content)


def main():
    message = (
        "During regression testing on staging, the login page is not working properly in Chrome. "
        "I entered a valid username and password, clicked the Login button, and the page just kept loading. "
        "Expected result: user should land on the dashboard. Actual result: loading spinner stays forever. "
        "This is blocking our release testing today. Firefox seems to work fine."
    )

    try:
        ticket = ask_json(message, TICKET_SCHEMA)
    except Exception as e:
        print(f"First attempt failed: {e}. Retrying...")
        ticket = ask_json(message, TICKET_SCHEMA)

    print("\nSTRUCTURED TICKET\n", json.dumps(ticket, indent=2))

    jira = {
        "summary": ticket["title"],
        "priority": ticket["severity"],
        "labels": [ticket["module"], ticket["browser"], ticket["environment"]],
        "description": (
            f"Steps: {', '.join(ticket['steps_to_reproduce'])}"
            f"Expected: {ticket['expected_result']}"
            f"Actual: {ticket['actual_result']}"
            f"Suggested Action: {ticket['suggested_next_action']}"
        )
    }
    print("\nJIRA PAYLOAD\n", json.dumps(jira, indent=2))

    if ticket["release_blocker"]:
        slack = (
            f"Release Blocker Detected",
            f"Bug: {ticket['title']}",
            f"Module: {ticket['module']}",
            f"Severity: {ticket['severity']}",
            f"Environment: {ticket['environment']}",
            f"Suggested action: {ticket['suggested_next_action']}"
        )
        print("\nSLACK ALERT\n", json.dumps(slack, indent=2))


if __name__ == "__main__":
    main()