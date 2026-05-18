
import json
import os

from openai import OpenAI
from common import check_env


# -----------------------------
# TEST CASE JSON SCHEMA
# -----------------------------
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
                    "type": {
                        "type": "string",
                        "enum": ["positive", "negative", "edge"]
                    },
                    "preconditions": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "steps": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "expected_result": {"type": "string"},
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"]
                    }
                },
                "required": [
                    "id",
                    "title",
                    "type",
                    "preconditions",
                    "steps",
                    "expected_result",
                    "priority"
                ],
                "additionalProperties": False
            }
        },
        "edge_cases": {
            "type": "array",
            "items": {"type": "string"}
        },
        "missing_requirements": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["feature", "test_cases", "edge_cases", "missing_requirements"],
    "additionalProperties": False
}


# -----------------------------
# INPUT REQUIREMENT
# -----------------------------
REQUIREMENT = """
Users should be able to reset their password using an OTP sent to their registered email.
The OTP should expire after 10 minutes.
If the user enters the wrong OTP three times, the account should be temporarily locked.
"""


# -----------------------------
# OPENAI CALL
# -----------------------------
def generate_test_cases(requirement: str):
    check_env()

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5.4-nano"),
        instructions="""
You are a QA test case generator.

Rules:
- Generate positive, negative, and edge test cases
- Do NOT guess missing details
- Put unclear requirements in missing_requirements
- Return only valid JSON matching schema
""",
        input=requirement,
        text={
            "format": {
                "type": "json_schema",
                "name": "test_case_output",
                "schema": TEST_CASE_SCHEMA,
                "strict": True
            }
        }
    )

    return json.loads(response.output_text)


# -----------------------------
# VALIDATION
# -----------------------------
def validate_output(data):
    if "test_cases" not in data:
        return False

    for tc in data["test_cases"]:
        required = ["id", "title", "type", "steps", "expected_result", "priority"]

        for field in required:
            if field not in tc:
                print("Missing:", field)
                return False

        if tc["type"] not in ["positive", "negative", "edge"]:
            print("Invalid type")
            return False

        if not isinstance(tc["steps"], list):
            print("Steps must be list")
            return False

    return True


# -----------------------------
# TEST MANAGEMENT PAYLOAD
# -----------------------------
def build_test_management(data):
    return {
        "suite_name": data["feature"],
        "test_cases": [
            {
                "title": tc["title"],
                "priority": tc["priority"],
                "steps": tc["steps"],
                "expected_result": tc["expected_result"]
            }
            for tc in data["test_cases"]
        ]
    }


# -----------------------------
# COVERAGE SUMMARY
# -----------------------------
def build_coverage_summary(data):
    return {
        "positive_cases": sum(tc["type"] == "positive" for tc in data["test_cases"]),
        "negative_cases": sum(tc["type"] == "negative" for tc in data["test_cases"]),
        "edge_cases": sum(tc["type"] == "edge" for tc in data["test_cases"]),
        "missing_requirements_count": len(data["missing_requirements"])
    }


# -----------------------------
# MAIN
# -----------------------------
def main():
    result = generate_test_cases(REQUIREMENT)

    if not validate_output(result):
        print("Validation failed")
        return

    print("\n📌 STRUCTURED TEST CASES:\n")
    print(json.dumps(result, indent=2))

    print("\n📦 TEST MANAGEMENT PAYLOAD:\n")
    print(json.dumps(build_test_management(result), indent=2))

    print("\n📊 COVERAGE SUMMARY:\n")
    print(json.dumps(build_coverage_summary(result), indent=2))


if __name__ == "__main__":
    main()