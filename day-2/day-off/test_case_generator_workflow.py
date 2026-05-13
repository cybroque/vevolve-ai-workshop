import json
import os
from openai import OpenAI
from common import check_env # Accessing your existing common file

# Define the JSON Schema for Structured Outputs
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
                    "type": {"type": "string", "enum": ["positive", "negative", "edge"]},
                    "preconditions": {"type": "array", "items": {"type": "string"}},
                    "steps": {"type": "array", "items": {"type": "string"}},
                    "expected_result": {"type": "string"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high"]}
                },
                # 'preconditions' must be added here to satisfy "strict": True
                "required": [
                    "id", "title", "type", "preconditions", 
                    "steps", "expected_result", "priority"
                ],
                "additionalProperties": False,
            }
        },
        "edge_cases": {"type": "array", "items": {"type": "string"}},
        "missing_requirements": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["feature", "test_cases", "edge_cases", "missing_requirements"],
    "additionalProperties": False,
}

def generate_test_suite(requirement_text):
    # Ensure environment is valid
    check_env()
    
    # Initialize the client using your preferred pattern
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Use the model from env or your gpt-5.4-nano default
    model_name = os.getenv("OPENAI_MODEL", "gpt-5.4-nano")

    prompt = f"Convert this requirement into a structured test suite:\n\n{requirement_text}"

    # Use 'client' here to create the response
    # Using the 'responses.create' pattern from your reference code
    response = client.responses.create(
        model=model_name,
        instructions="Return a valid JSON object matching the provided schema. Do not include markdown formatting.",
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "test_case_generation",
                "schema": TEST_CASE_SCHEMA,
                "strict": True,
            }
        },
    )

    # Parse the output_text into a Python dictionary
    structured_data = json.loads(response.output_text)
    return structured_data

def main():
    starter_input = (
        "Users should be able to reset their password using an OTP sent to their registered email. "
        "The OTP should expire after 10 minutes. "
        "If the user enters the wrong OTP three times, the account should be temporarily locked."
    )

    print("Generating test cases...")
    try:
        # 1. Get the structured JSON
        test_data = generate_test_suite(starter_input)

        # 2. Prepare Test-Management Payload
        management_payload = {
            "suite_name": test_data["feature"],
            "test_cases": [
                {
                    "title": tc["title"],
                    "priority": tc["priority"],
                    "steps": tc["steps"],
                    "expected_result": tc["expected_result"]
                } for tc in test_data["test_cases"]
            ]
        }

        # 3. Generate Coverage Summary
        summary = {
            "positive_cases": len([tc for tc in test_data["test_cases"] if tc["type"] == "positive"]),
            "negative_cases": len([tc for tc in test_data["test_cases"] if tc["type"] == "negative"]),
            "edge_cases": len(test_data["edge_cases"]),
            "missing_requirements_count": len(test_data["missing_requirements"])
        }

        # Output Results
        print("\n--- Structured JSON ---")
        print(json.dumps(test_data, indent=2))
        
        print("\n--- Test Management Payload ---")
        print(json.dumps(management_payload, indent=2))
        
        print("\n--- Coverage Summary ---")
        print(json.dumps(summary, indent=2))

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()