import json
import os
import sys
from pathlib import Path

from common import check_env
from openai import OpenAI

sys.path.append(str(Path(__file__).resolve().parents[2]))


QA_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "module": {"type": "string"},
        "environment": {"type": "string"},
        "browser": {"type": "string"},
        "severity": {"type": "string","enum": ["low", "medium", "high"]},
        "release_blocker": {"type": "boolean"},
        "steps_to_reproduce": {"type": "array","items": {"type": "string"}},
        "expected_result": {"type": "string"},
        "actual_result": {"type": "string"},
        "missing_information": {"type": "array","items": {"type": "string"}},
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
    "additionalProperties": False,
}



def ask_json(prompt, schema, *, name="result"):
    check_env()
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )
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



def validate_ticket(ticket):
    required_fields = [
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
    ]
    for field in required_fields:
        if field not in ticket:
            print(f"Missing required field: {field}")
            return False
    allowed_severity = ["low", "medium", "high"]
    if ticket["severity"] not in allowed_severity:
        print("Invalid severity value")
        return False
    if not isinstance(ticket["steps_to_reproduce"], list):
        print("steps_to_reproduce must be a list")
        return False
    if not isinstance(ticket["release_blocker"], bool):
        print("release_blocker must be boolean")
        return False
    if not isinstance(ticket["missing_information"], list):
        print("missing_information must be a list")
        return False
    return True



def extract_ticket(message: str):
    prompt = f"""
    You are QA triage assistant
    Convert the following support message into a structured bug ticket.
    Return only valid JSON that matches the schema.
    If information is missing or unclear, add it to missing_information.
    Support Message:
    {message}
    """
    try:
        ticket = ask_json(prompt, QA_SCHEMA, name="support_ticket")
        if validate_ticket(ticket):
            return ticket
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"First attempt failed: {exc}")
        try:
            ticket = ask_json(prompt, QA_SCHEMA, name="support_ticket")
            if validate_ticket(ticket):
                return ticket
        except (json.JSONDecodeError, ValueError) as exc:
            print(f"Retry failed: {exc}")
    return None



def generate_jira_payload(ticket):
    return {
        "summary": ticket["title"],
        "priority": ticket["severity"],
        "labels": [
            ticket["module"],
            ticket["browser"],
            ticket["environment"]
        ],
        "description": (
            f"Steps to Reproduce:"
            f"{ticket['steps_to_reproduce']}"
            f"Expected Result:"
            f"{ticket['expected_result']}"
            f"Actual Result:"
            f"{ticket['actual_result']}"
            f"Suggested Next Action:"
            f"{ticket['suggested_next_action']}"
        )
    }



def generate_slack_alert(ticket):
    if not ticket["release_blocker"]:
        return None
    return f"""
Release Blocker Detected

Bug: {ticket['title']}
Module: {ticket['module']}
Severity: {ticket['severity']}
Environment: {ticket['environment']}

Suggested action:
{ticket['suggested_next_action']}
"""



def main():
    message = (
        "During regression testing on staging, the login page is not "
        "working properly in Chrome. "
        "I entered a valid username and password, clicked the Login "
        "button, and the page just kept loading. "
        "Expected result: user should land on the dashboard. "
        "Actual result: loading spinner stays forever. "
        "This is blocking our release testing today. "
        "Firefox seems to work fine."
    )
    ticket = extract_ticket(message)
    if not ticket:
        print("Failed to generate valid structured ticket.")
        return
    slack_alert = generate_slack_alert(ticket)
    if slack_alert:
        print(slack_alert)
    print(json.dumps(ticket, indent=2))
    jira_payload = generate_jira_payload(ticket)
    print(json.dumps(jira_payload, indent=2))
if __name__ == "__main__":
    main()