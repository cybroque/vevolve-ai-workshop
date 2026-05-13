import json
import os
from test import check_env
from openai import OpenAI

# --- JSON Schema for Test Cases ---
TEST_CASE_SCHEMA = {
    "type": "object",
    "properties": {
        "feature": {"type": "string"},
        "test_cases": {
            "type": "array",
            "maxItems": 3,
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "title": {"type": "string"},
                    "type": {"type": "string", "enum": ["positive", "negative", "edge"]},
                    "preconditions": {"type": "array", "items": {"type": "string"}},
                    "steps": {"type": "array", "items": {"type": "string"}},
                    "expected_result": {"type": "string"},
                    "priority": {"type": "string"}
                },
                #  include all keys here
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
        "edge_cases": {"type": "array", "items": {"type": "string"}},
        "missing_requirements": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["feature", "test_cases", "edge_cases", "missing_requirements"],
    "additionalProperties": False
}

# --- Starter Requirement ---
requirement = (
    "Users should be able to reset their password using an OTP sent to their registered email. "
    "The OTP should expire after 10 minutes. "
    "If the user enters the wrong OTP three times, the account should be temporarily locked."
)


# --- Separate Validation Function ---
def validate_test_cases(structured_output):
    if not isinstance(structured_output.get("test_cases"), list):
        print(" test_cases must be a list")
        return False

    for tc in structured_output["test_cases"]:
        for field in ["id", "title", "type", "steps", "expected_result", "priority"]:
            if field not in tc:
                print(f" Missing field in test case: {field}")
                return False
        if not isinstance(tc["steps"], list):
            print(" steps must be a list")
            return False
        if tc["type"] not in ["positive", "negative", "edge"]:
            print(" type must be one of: positive, negative, edge")
            return False
    return True


def main():
    check_env()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # --- Step 1: Extract structured test cases ---
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5.4-nano"),
        instructions="Convert the requirement into structured test cases. Return only valid JSON matching schema.",
        input=requirement,
        text={
            "format": {
                "type": "json_schema",
                "name": "test_cases",
                "schema": TEST_CASE_SCHEMA,
                "strict": True,
            }
        },
    )

    #print("Raw JSON Output:", response.output_text)

    try:
        structured_output = json.loads(response.output_text)
    except json.JSONDecodeError:
        print(" Invalid JSON returned by model.")
        return

    # --- Step 2: Validation ---
    if not validate_test_cases(structured_output):
        return

    print("Structured Test Cases are valid!")
    print("Parsed Output:", json.dumps(structured_output, indent=2))

    # --- Step 3: Test-management payload ---
    payload = {
        "suite_name": structured_output["feature"],
        "test_cases": [
            {
                "title": tc["title"],
                "priority": tc["priority"],
                "steps": tc["steps"],
                "expected_result": tc["expected_result"]
            }
            for tc in structured_output["test_cases"]
        ]
    }

    print("Payload")
    print("Test-management Payload:", json.dumps(payload, indent=2))

    # --- Step 4: Coverage summary ---
    coverage = {
        "positive_cases": sum(1 for tc in structured_output["test_cases"] if tc["type"] == "positive"),
        "negative_cases": sum(1 for tc in structured_output["test_cases"] if tc["type"] == "negative"),
        "edge_cases": sum(1 for tc in structured_output["test_cases"] if tc["type"] == "edge"),
        "missing_requirements_count": len(structured_output["missing_requirements"])
    }
    print("Coverage Summary:", json.dumps(coverage, indent=2))
    

if _name_ == "_main_":
    main()