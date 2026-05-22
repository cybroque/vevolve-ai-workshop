"""
Enforce structured output with JSON Schema.
Day 2, Session 4: Structured Outputs Part A

Learning Objective:
Use schema-shaped output for code-readable responses.
"""

import json
import os

from common import check_env
from openai import OpenAI


TESTCASE_SCHEMA = {
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
                    "type": {"type": "string"},
                    "preconditions": {"type": "array"},
                    "steps": {"type": "array"},
                    "expected_result": {"type": "string"},
                    "priority": {"type": "string"},
                },
                "required": [
                    "id",
                    "title",
                    "type",
                    "steps",
                    "expected_result"
                ],
            },
        },

        "edge_cases": {
            "type": "array"
        },

        "missing_requirements": {
            "type": "array"
        },
    },

    "required": [
        "feature",
        "test_cases",
        "edge_cases",
        "missing_requirements"
    ],

    "additionalProperties": False,
}


def main():

    check_env()

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    requirement = """
    Users should be able to reset their password using an OTP
    sent to their registered email.

    The OTP should expire after 10 minutes.

    If the user enters the wrong OTP three times,
    the account should be temporarily locked.
    """

    data = client.responses.create(

        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),

        instructions="""
        Generate structured test cases from the requirement.
        Include positive, negative, and edge test cases.
        Return only valid JSON.
        """,

        input=requirement,

        text={
            "format": {
                "type": "json_schema",
                "name": "test_cases",
                "schema": TESTCASE_SCHEMA,
                "strict": True,
            }
        },
    )

    print("JSON Output:")
    print(data.output_text)

    result = json.loads(data.output_text)

    print("\nParsed Output:")
    print(json.dumps(result, indent=2))

    # Coverage Summary
    print("\nCoverage Summary")

    print("Total Test Cases:", len(result["test_cases"]))

    print("Edge Cases:", len(result["edge_cases"]))


if __name__ == "__main__":
    main()