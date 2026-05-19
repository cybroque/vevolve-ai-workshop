import json
import os
import sys
from pathlib import Path

from common import check_env
from openai import OpenAI

sys.path.append(str(Path(__file__).resolve().parents[2]))


TEST_CASE_SCHEMA = {
    "type": "object",
    "properties": {
        "feature": {"type": "string"},
        "test_cases": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "title": {"type": "string"},
                    "type": {"type": "string","enum": ["positive", "negative", "edge"]},
                    "preconditions": {"type": "array","items": {"type": "string"}}, 
                    "steps": {"type": "array","items": {"type": "string"}},
                    "expected_result": {"type": "string"},
                    "priority": {"type": "string","enum": ["low", "medium", "high"]}
                },
                "required": ["id","title","type","preconditions","steps","expected_result","priority"],
                "additionalProperties": False
            }
        },
        "edge_cases": {"type": "array","items": {"type": "string"}},
        "missing_requirements": {"type": "array","items": {"type": "string"}}
    },
    "required": ["feature","test_cases","edge_cases","missing_requirements"],
    "additionalProperties": False
}


def ask_json(prompt, schema, *, name="result"):
    check_env()
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    response = client.responses.create(
        model="gpt-5.4-nano",
        instructions="Return only valid JSON matching the schema.",
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


def validate_test_cases(data):
    required_fields = ["feature","test_cases","edge_cases","missing_requirements"]
    for field in required_fields:
        if field not in data:
            print(f"Missing field: {field}")
            return False
    if not isinstance(data["test_cases"], list):
        print("test_cases must be a list")
        return False
    allowed_types = ["positive", "negative", "edge"]
    for test_case in data["test_cases"]:
        required_test_case_fields = ["id","title","type","steps","expected_result","priority"]
        for field in required_test_case_fields:
            if field not in test_case:
                print(f"Missing test case field: {field}")
                return False
        if test_case["type"] not in allowed_types:
            print("Invalid test case type")
            return False
        if not isinstance(test_case["steps"], list):
            print("steps must be a list")
            return False
    return True


def extract_test_cases(requirement: str):
    prompt = f"""
    You are a QA test case generator assistant.
    Convert the following product requirement into structured test cases.
    Rules:
    - Return only valid JSON
    - Generate positive, negative, and edge test cases
    - Add unclear requirements into missing_requirements
    - Steps should be clear and readable
    Product Requirement:
    {requirement}
    """
    try:
        result = ask_json(prompt,TEST_CASE_SCHEMA,name="test_case_result")
        if validate_test_cases(result):
            return result
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"First attempt failed: {exc}")
        try:
            result = ask_json(prompt,TEST_CASE_SCHEMA,name="test_case_result")
            if validate_test_cases(result):
                return result
        except (json.JSONDecodeError, ValueError) as exc:
            print(f"Retry failed: {exc}")
    return None


def generate_test_management_payload(data):
    payload_test_cases = []
    for test_case in data["test_cases"]:
        payload_test_cases.append({
            "title": test_case["title"],
            "priority": test_case["priority"],
            "steps": test_case["steps"],
            "expected_result": test_case["expected_result"]
        })
    return {
        "suite_name": data["feature"],
        "test_cases": payload_test_cases
    }


def generate_coverage_summary(data):
    positive_cases = 0
    negative_cases = 0
    edge_cases = 0
    for test_case in data["test_cases"]:
        if test_case["type"] == "positive":
            positive_cases += 1
        elif test_case["type"] == "negative":
            negative_cases += 1
        elif test_case["type"] == "edge":
            edge_cases += 1
    return {
        "positive_cases": positive_cases,
        "negative_cases": negative_cases,
        "edge_cases": edge_cases,
        "missing_requirements_count":
            len(data["missing_requirements"])
    }


def main():
    requirement = (
        "Users should be able to reset their password "
        "using an OTP sent to their registered email. "
        "The OTP should expire after 10 minutes. "
        "If the user enters the wrong OTP three times, "
        "the account should be temporarily locked."
    )
    result = extract_test_cases(requirement)
    if not result:
        print("Failed to generate valid test cases")
        return
    print(json.dumps(result, indent=2))
    test_management_payload = generate_test_management_payload(result)
    print(json.dumps(test_management_payload, indent=2))
    coverage_summary = generate_coverage_summary(result)
    print(json.dumps(coverage_summary, indent=2))

if __name__ == "__main__":
    main()