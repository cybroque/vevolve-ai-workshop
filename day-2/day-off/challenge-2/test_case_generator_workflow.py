# test_case_generator_workflow.py

from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

requirement = """
Users should be able to reset their password using an OTP sent to their registered email.
The OTP should expire after 10 minutes.
If the user enters the wrong OTP three times, the account should be temporarily locked.
"""

prompt = f"""
You are an expert QA Test Case Generator.

Analyze the product requirement below and generate structured test cases.

IMPORTANT RULES:
- Return ONLY valid JSON
- Do NOT include markdown
- Do NOT guess unclear requirements
- Add unclear or missing details to missing_requirements
- Generate positive, negative, and edge test cases
- test_cases must be a list
- steps must be a list
- type must be one of:
  positive, negative, edge
- priority should be:
  low, medium, or high

Required JSON format:

{{
  "feature": "",
  "test_cases": [
    {{
      "id": "TC001",
      "title": "",
      "type": "positive",
      "preconditions": [],
      "steps": [],
      "expected_result": "",
      "priority": "medium"
    }}
  ],
  "edge_cases": [],
  "missing_requirements": []
}}

Product Requirement:
{requirement}
"""

try:

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a professional QA automation assistant."
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

    data = json.loads(ai_output)

except json.JSONDecodeError:

    print("ERROR: AI returned invalid JSON")

    print("\nRaw AI Output:\n")
    print(ai_output)

    exit()

validation_errors = []

required_fields = [
    "feature",
    "test_cases",
    "edge_cases",
    "missing_requirements"
]

for field in required_fields:

    if field not in data:
        validation_errors.append(
            f"Missing required field: {field}"
        )

if "test_cases" in data:

    if not isinstance(data["test_cases"], list):
        validation_errors.append(
            "test_cases must be a list"
        )

valid_types = ["positive", "negative", "edge"]

valid_priorities = ["low", "medium", "high"]

required_test_case_fields = [
    "id",
    "title",
    "type",
    "steps",
    "expected_result",
    "priority"
]

if "test_cases" in data and isinstance(data["test_cases"], list):
    for index, tc in enumerate(data["test_cases"]):
        for field in required_test_case_fields:
            if field not in tc:
                validation_errors.append(
                    f"Test case {index + 1} missing field: {field}"
                )
        if "type" in tc:
            if tc["type"] not in valid_types:
                validation_errors.append(
                    f"Invalid test type in {tc.get('id', 'Unknown ID')}"
                )
        if "steps" in tc:
            if not isinstance(tc["steps"], list):
                validation_errors.append(
                    f"steps must be a list in {tc.get('id', 'Unknown ID')}"
                )
        if "priority" in tc:

            if tc["priority"] not in valid_priorities:
                validation_errors.append(
                    f"Invalid priority in {tc.get('id', 'Unknown ID')}"
                )

print("\n================ VALIDATION RESULT ================\n")

if validation_errors:

    print("Validation Failed:\n")

    for error in validation_errors:
        print(f"- {error}")

    exit()

else:

    print("Validation Successful")

test_management_payload = {
    "suite_name": data["feature"],
    "test_cases": []
}

for tc in data["test_cases"]:

    test_management_payload["test_cases"].append(
        {
            "title": tc["title"],
            "priority": tc["priority"],
            "steps": tc["steps"],
            "expected_result": tc["expected_result"]
        }
    )

coverage_summary = {
    "positive_cases": 0,
    "negative_cases": 0,
    "edge_cases": 0,
    "missing_requirements_count": len(data["missing_requirements"])
}

for tc in data["test_cases"]:

    if tc["type"] == "positive":
        coverage_summary["positive_cases"] += 1

    elif tc["type"] == "negative":
        coverage_summary["negative_cases"] += 1

    elif tc["type"] == "edge":
        coverage_summary["edge_cases"] += 1

print("\n================ STRUCTURED TEST CASE JSON ================\n")

print(json.dumps(data, indent=4))

print("\n================ TEST MANAGEMENT PAYLOAD ================\n")

print(json.dumps(test_management_payload, indent=4))

print("\n================ COVERAGE SUMMARY ================\n")

print(json.dumps(coverage_summary, indent=4))