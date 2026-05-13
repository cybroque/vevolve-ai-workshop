
structured_bug_workflow.py
--------------------------
AI Bug Triage Workflow

1. **Bug Report Input**  
   - A messy bug report is given (hard-coded for testing).  

2. **LLM Extraction**  
   - The bug report is converted into a structured JSON object.  
   - JSON Schema is used to enforce required fields.  

3. **Validation**  
   - Rules checked:  
     - `steps_to_reproduce` must be a list  
     - `release_blocker` must be a boolean  
     - `severity` must be one of: low / medium / high  

4. **Jira Payload**  
   - A Jira-style payload is created from the structured bug object.  

5. **Slack Alert**  
   - If `release_blocker` is true, a Slack alert message is printed.  





test_case_generator_workflow.py
----------------------------------
AI Test Case Generator Workflow

## Overview
This project demonstrates how to convert a messy product requirement into structured test cases using AI.  
The workflow enforces a JSON Schema so that the output is always code‑readable and valid.

## Workflow Steps
1. **Requirement Input**  
   - Accept a product requirement as plain text.

2. **Feature Extraction**  
   - Identify the main feature name from the requirement.

3. **Test Case Generation**  
   - Generate exactly 3 test cases:
     - 1 Positive
     - 1 Negative
     - 1 Edge

4. **Validation**  
   - A separate function `validate_test_cases()` checks:
     - `test_cases` must be a list.
     - Each test case must include: `id`, `title`, `type`, `preconditions`, `steps`, `expected_result`, `priority`.
     - `steps` must be a list.
     - `type` must be one of: positive, negative, edge.

5. **Test-management Payload**  
   - Create a simplified payload with suite name and test cases for tools like Jira/TestRail.

6. **Coverage Summary**  
   - Count positive, negative, edge cases.
   - Count missing requirements.

---

## Validation
- Ensures strict JSON Schema compliance.
- Prevents invalid or incomplete test cases.
- Keeps workflow predictable and tool‑friendly.

---

## What Could Go Wrong
- **Invalid JSON**: Model may return malformed JSON.
- **Missing Fields**: Some test cases may not include required keys.
- **Wrong Data Types**: Steps may appear as a string instead of a list.
- **Wrong Case Types**: Type may not match allowed values (positive, negative, edge).
- **Incomplete Requirements**: Missing requirements may not be captured, leading to test gaps.

---

