from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

bug_report = """
During regression testing on staging, the login page is not working properly in Chrome.
I entered a valid username and password, clicked the Login button, and the page just kept loading.
Expected result: user should land on the dashboard.
Actual result: loading spinner stays forever.
This is blocking our release testing today. Firefox seems to work fine.
"""

prompt = f"""
You are a QA triage assistant.

Analyze the bug report below and extract structured bug information.

IMPORTANT RULES:
- Return ONLY valid JSON.
- Do NOT include markdown.
- Do NOT guess missing information.
- If information is unclear or missing, add it to missing_information.
- severity must be one of:
  low, medium, high, critical
- release_blocker must be true or false
- steps_to_reproduce must be an array

Required JSON format:

{{
  "title": "",
  "module": "",
  "environment": "",
  "browser": "",
  "severity": "",
  "release_blocker": false,
  "steps_to_reproduce": [],
  "expected_result": "",
  "actual_result": "",
  "missing_information": [],
  "suggested_next_action": ""
}}

Bug Report:
{bug_report}
"""

try:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert QA bug triage assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    ai_output = response.choices[0].message.content

except Exception as e:
    print("Error while calling OpenAI API:")
    print(e)
    exit()

try:
    bug_data = json.loads(ai_output)

except json.JSONDecodeError:
    print("ERROR: AI returned invalid JSON")
    print("\nRaw AI Output:\n")
    print(ai_output)
    exit()

validation_errors = []

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
    if field not in bug_data:
        validation_errors.append(f"Missing required field: {field}")

valid_severity = ["low", "medium", "high", "critical"]

if "severity" in bug_data:
    if bug_data["severity"] not in valid_severity:
        validation_errors.append(
            "severity must be one of: low, medium, high, critical"
        )

if "release_blocker" in bug_data:
    if not isinstance(bug_data["release_blocker"], bool):
        validation_errors.append(
            "release_blocker must be a boolean"
        )

if "steps_to_reproduce" in bug_data:
    if not isinstance(bug_data["steps_to_reproduce"], list):
        validation_errors.append(
            "steps_to_reproduce must be a list"
        )

if "missing_information" in bug_data:
    if not isinstance(bug_data["missing_information"], list):
        validation_errors.append(
            "missing_information must be a list"
        )


print("\n================ VALIDATION RESULT ================\n")

if validation_errors:
    print("Validation Failed:\n")

    for error in validation_errors:
        print(f"- {error}")

    exit()

else:
    print("Validation Successful")


jira_payload = {
    "summary": bug_data["title"],
    "priority": bug_data["severity"],
    "labels": [
        bug_data["module"],
        bug_data["browser"],
        bug_data["environment"]
    ],
    "description": f"""
Steps to Reproduce:
{chr(10).join(bug_data['steps_to_reproduce'])}

Expected Result:
{bug_data['expected_result']}

Actual Result:
{bug_data['actual_result']}

Suggested Next Action:
{bug_data['suggested_next_action']}
"""
}

print("\n================ STRUCTURED BUG JSON ================\n")

print(json.dumps(bug_data, indent=4))

print("\n================ JIRA PAYLOAD ================\n")

print(json.dumps(jira_payload, indent=4))

if bug_data["release_blocker"]:

    slack_alert = f"""
================ SLACK ALERT ================

Release Blocker Detected

Bug: {bug_data['title']}
Module: {bug_data['module']}
Severity: {bug_data['severity']}
Environment: {bug_data['environment']}

Suggested Action:
{bug_data['suggested_next_action']}
"""

    print(slack_alert)

else:
    print("\nNo release blocker detected. Slack alert not generated.")