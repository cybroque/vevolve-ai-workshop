
import json
import re
import os
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.json import JSON

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
console = Console()


MESSY_REQUIREMENT = """
Users should be able to reset their password using an OTP sent to their registered email.
The OTP should expire after 10 minutes. If the user enters the wrong OTP three times,
the account should be temporarily locked.
"""

def extract_test_cases(requirement: str) -> dict:
    """Send messy requirement to OpenAI and extract structured test cases."""

    system_prompt = """You are a QA engineer. Generate structured test cases from product requirements.
Return ONLY valid JSON, no markdown, no explanation, no code fences.
type must be one of: positive, negative, edge.
steps must be a list of strings (clear actions).
priority must be one of: low, medium, high, critical.
missing_requirements should capture unclear or assumed details."""

    user_prompt = f"""Convert the following requirement into this exact JSON structure:
{{
  "feature": "Password reset using OTP",
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

Generate at least 2 positive, 2 negative, and 2 edge test cases.
Each test case must have: id, title, type, preconditions, steps, expected_result, priority.

Requirement:
{requirement}"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt}
        ],
        temperature=0
    )

    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"```json|```", "", raw).strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        console.print(f"[bold red][ERROR] Failed to parse LLM response as JSON: {e}[/bold red]")
        console.print(f"[yellow][RAW RESPONSE]\n{raw}[/yellow]")
        return {}

def validate_test_cases(data: dict) -> list:
    """Validate required fields in each test case. Returns list of errors."""
    errors = []

    if "test_cases" not in data:
        errors.append("Missing top-level field: 'test_cases'")
        return errors

    if not isinstance(data["test_cases"], list):
        errors.append("'test_cases' must be a list")
        return errors

    required_tc_fields = ["id", "title", "type", "steps", "expected_result", "priority"]
    valid_types = ["positive", "negative", "edge"]

    for i, tc in enumerate(data["test_cases"]):
        for field in required_tc_fields:
            if field not in tc:
                errors.append(f"Test case {i+1}: missing field '{field}'")

        if "type" in tc and tc["type"] not in valid_types:
            errors.append(f"Test case {i+1}: 'type' must be one of {valid_types}. Got: '{tc['type']}'")

        if "steps" in tc and not isinstance(tc["steps"], list):
            errors.append(f"Test case {i+1}: 'steps' must be a list")

    return errors

def generate_test_management_payload(data: dict) -> dict:
    """Generate a test-management-style payload."""
    return {
        "suite_name": data.get("feature", "Unknown Feature"),
        "test_cases": [
            {
                "title": tc.get("title", "Untitled"),
                "priority": tc.get("priority", "medium"),
                "steps": tc.get("steps", []),
                "expected_result": tc.get("expected_result", "")
            }
            for tc in data.get("test_cases", [])
        ]
    }

def generate_coverage_summary(data: dict) -> dict:
    """Generate a coverage summary from test cases."""
    test_cases = data.get("test_cases", [])
    return {
        "positive_cases": sum(1 for tc in test_cases if tc.get("type") == "positive"),
        "negative_cases": sum(1 for tc in test_cases if tc.get("type") == "negative"),
        "edge_cases":     sum(1 for tc in test_cases if tc.get("type") == "edge"),
        "missing_requirements_count": len(data.get("missing_requirements", []))
    }

def run_test_case_workflow(requirement: str):

    console.print(Panel("[bold blue]STEP 1: Extracting structured test cases from requirement...[/bold blue]"))
    structured = extract_test_cases(requirement)

    if not structured:
        console.print("[bold red][WORKFLOW STOPPED] Could not extract structured data.[/bold red]")
        return

    console.print(JSON(json.dumps(structured, indent=2)))

    console.print(Panel("[bold blue]STEP 2: Validating test case structure...[/bold blue]"))
    errors = validate_test_cases(structured)
    if errors:
        for e in errors:
            console.print(f"  [red]❌ {e}[/red]")
    else:
        console.print("  [green]✅ All test cases valid![/green]")

    if structured.get("missing_requirements"):
        console.print("\n[bold yellow][MISSING REQUIREMENTS DETECTED][/bold yellow]")
        for item in structured["missing_requirements"]:
            console.print(f"  [yellow]⚠️  {item}[/yellow]")

    console.print(Panel("[bold blue]STEP 3: Generating test management payload...[/bold blue]"))
    tm_payload = generate_test_management_payload(structured)
    console.print(JSON(json.dumps(tm_payload, indent=2)))

    console.print(Panel("[bold blue]STEP 4: Coverage summary...[/bold blue]"))
    summary = generate_coverage_summary(structured)
    console.print(JSON(json.dumps(summary, indent=2)))

    console.print(Panel("[bold green]✅ WORKFLOW COMPLETE[/bold green]"))


if __name__ == "__main__":
    run_test_case_workflow(MESSY_REQUIREMENT)