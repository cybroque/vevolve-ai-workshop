import json
import os
import sys
from pathlib import Path

from common import check_env
from openai import OpenAI

sys.path.append(str(Path(__file__).resolve().parents[2]))

# Schema for structured test case extraction
TEST_SCHEMA = {
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
                    "type": {"type": "string", "enum": ["positive", "negative", "edge"]},
                    "preconditions": {"type": "array", "items": {"type": "string"}},
                    "steps": {"type": "array", "items": {"type": "string"}},
                    "expected_result": {"type": "string"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high"]},
                },
                "required": ["id", "title", "type", "preconditions", "steps", "expected_result", "priority"],
                "additionalProperties": False
            },
        },
        "edge_cases": {"type": "array", "items": {"type": "string"}},
        "missing_requirements": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["feature", "test_cases", "edge_cases", "missing_requirements"],
    "additionalProperties": False,
}


def ask_json(prompt, schema, *, name="structured_test_cases"):
    """Send prompt to LLM and return structured JSON."""
    check_env()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
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


def validate_test_report(report):
    """Validate that extracted test cases meet schema rules."""
    required_fields = ["feature", "test_cases", "edge_cases", "missing_requirements"]
    for field in required_fields:
        if field not in report:
            print(f"Missing field: {field}")
            return False
    if not isinstance(report["test_cases"], list):
        print("test_cases must be a list")
        return False
    allowed_types = ["positive", "negative", "edge"]
    for tc in report["test_cases"]:
        for field in ["id", "title", "type", "steps", "expected_result", "priority"]:
            if field not in tc:
                print(f"Missing test case field: {field}")
                return False
        if tc["type"] not in allowed_types:
            print("Invalid test case type")
            return False
        if not isinstance(tc["steps"], list):
            print("steps must be a list")
            return False
    return True


def extract_test_report(requirement: str):
    """Extract structured test cases from messy requirement text."""
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
        report = ask_json(prompt, TEST_SCHEMA, name="structured_test_cases")
        if validate_test_report(report):
            return report
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"First attempt failed: {exc}")
        try:
            report = ask_json(prompt, TEST_SCHEMA, name="structured_test_cases")
            if validate_test_report(report):
                return report
        except (json.JSONDecodeError, ValueError) as exc:
            print(f"Retry failed: {exc}")
    return None


def build_test_management_payload(report):
    """Generate test-management-style payload."""
    payload_cases = []
    for tc in report["test_cases"]:
        payload_cases.append({
            "title": tc["title"],
            "priority": tc["priority"],
            "steps": tc["steps"],
            "expected_result": tc["expected_result"]
        })
    return {
        "suite_name": report["feature"],
        "test_cases": payload_cases
    }


def build_coverage_summary(report):
    """Generate coverage summary counts."""
    return {
        "positive_cases": sum(1 for tc in report["test_cases"] if tc["type"] == "positive"),
        "negative_cases": sum(1 for tc in report["test_cases"] if tc["type"] == "negative"),
        "edge_cases": sum(1 for tc in report["test_cases"] if tc["type"] == "edge"),
        "missing_requirements_count": len(report["missing_requirements"])
    }


def main():
    requirement = (
        "Users should be able to reset their password "
        "using an OTP sent to their registered email. "
        "The OTP should expire after 10 minutes. "
        "If the user enters the wrong OTP three times, "
        "the account should be temporarily locked."
    )
    report = extract_test_report(requirement)
    if not report:
        print("Failed to generate valid test cases")
        return

    print("Structured Test Report:")
    print(json.dumps(report, indent=2))

    test_payload = build_test_management_payload(report)
    print("\nTest-Management Payload:")
    print(json.dumps(test_payload, indent=2))

    coverage = build_coverage_summary(report)
    print("\nCoverage Summary:")
    print(json.dumps(coverage, indent=2))


if __name__ == "__main__":
    main()
