


"""Enforce structured output with JSON Schema.
Day 2, Session 4: Structured Outputs Part A
Learning Objective: Use schema-shaped output for code-readable responses.
"""

import json
import os

from common import check_env
from openai import OpenAI

PRODUCT_SCHEMA = {
    "type": "object",
    "properties": {
        "product_name": {"type": "string"},
        "price": {"type": "number"},
        "in_stock": {"type": "boolean"},
        "tags": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": [
        "product_name",
        "price",
        "in_stock",
        "tags"
    ],
    "additionalProperties": False,
}


def main():
    check_env()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    data = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5.4-nano"),
        instructions="Return only data that matches the provided JSON schema.",
        input="The iPhone 15 costs 799 dollars, is available, and belongs to electronics and mobile categories.",
        text={
            "format": {
                "type": "json_schema",
                "name": "product",
                "schema": PRODUCT_SCHEMA,
                "strict": True,
            }
        },
    )
    print("JSON Output:", data.output_text)

    result = json.loads(data.output_text)
    print("Parsed Output:", result)


if __name__ == "__main__":
    main()