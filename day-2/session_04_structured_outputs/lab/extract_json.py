import json
import os
from common import check_env
from openai import OpenAI

# 1. Define a more complex schema
SERVICE_SCHEMA = {
    "type": "object",
    "properties": {
        "vehicle_name": {"type": "string"},
        "odometer_km": {"type": "integer"},
        "services_performed": {
            "type": "array",
            "items": {"type": "string"}
        },
        "next_service_due": {"type": "string"}
    },
    "required": ["vehicle_name", "odometer_km", "services_performed", "next_service_due"],
    "additionalProperties": False,
}

def main():
    check_env()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Simulating a messy real-world input
    raw_input = """
    The Vida VX2 Plus was brought in today at 4500km. 
    We performed a full battery health check, tightened the brakes, 
    and updated the firmware to version 2.4. 
    The customer should return after another 5000km.
    """
    try:

        data = client.responses.create(
            model="gpt-5.4-nano",
            instructions="Extract vehicle service data into the required JSON format.",
            input=raw_input,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "service_report",
                    "schema": SERVICE_SCHEMA,
                    "strict": True,
                }
            },
        )
        print("JSON Output:", data.output_text)
        result = json.loads(data.output_text)
        print("Parsed Output:", result)
    except Exception as e:
        print("Error occurred:", str(e))

if __name__ == "__main__":
    main()