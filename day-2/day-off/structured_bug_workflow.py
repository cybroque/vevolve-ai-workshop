import json
import os
from openai import OpenAI
from common import check_env

BUG_REPORT_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "module": {"type": "string"},
        "environment": {"type": "string"},
        "browser": {"type": "string"},
        "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
        "release_blocker": {"type": "boolean"},
        "steps_to_reproduce": {"type": "array", "items": {"type": "string"}},
        "expected_result": {"type": "string"},
        "actual_result": {"type": "string"},
        "missing_information": {"type": "array", "items": {"type": "string"}},
        "suggested_next_action": {"type": "string"},
    },
    "required": [
        "title", "module", "environment", "browser", "severity", 
        "release_blocker", "steps_to_reproduce", "expected_result", 
        "actual_result", "missing_information", "suggested_next_action"
    ],
    "additionalProperties": False,
}

def extract_bug_data(client, model, report_text):
    """Uses the passed client and model to extract data."""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Extract bug details into the required schema. If info is missing, list it in missing_information."},
                {"role": "user", "content": report_text}
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "bug_triage",
                    "schema": BUG_REPORT_SCHEMA,
                    "strict": True
                }
            }
        )
        
        content = response.choices[0].message.content or ""
        if not content:
            return {}
            
        return json.loads(content)
    except Exception as e:
        print(f"Extraction Error: {e}")
        return {}

def create_jira_payload(data):
    """Maps JSON data to Jira format."""
    return {
        "summary": data.get("title"),
        "priority": data.get("severity"),
        "labels": [data.get("module"), data.get("browser"), data.get("environment")],
        "description": f"Actual Result: {data.get('actual_result')}"
    }

def create_slack_alert(data):
    """Generates Slack text if it's a blocker."""
    if not data.get("release_blocker"):
        return None
    return f" Blocker: {data.get('title')} ({data.get('severity')})"

def main():
    check_env()
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", "gpt-4o") 

    raw_input = (
        "During regression testing on staging, the login page is not working properly in Chrome. "
        "The page just kept loading after clicking login. Blocking release testing."
    )

    # We pass client and model into the function here
    json_format = extract_bug_data(client, model, raw_input)
    
    if json_format:
        print("--- JSON format ---")
        print(json.dumps(json_format, indent=2))
        
        jira = create_jira_payload(json_format)
        print("\n--- Jira Payload ---")
        print(json.dumps(jira, indent=2))
        
        slack = create_slack_alert(json_format)
        if slack:
            print(f"\n--- Slack Alert ---\n{slack}")

if __name__ == "__main__":
    main()