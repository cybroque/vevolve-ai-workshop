# AI Test Case Generator Workflow

## 🔹 Overview
This project implements an AI-powered workflow that converts messy product requirements into structured test cases using a strict JSON schema.  
It also generates a test-management-style payload and a coverage summary.

The workflow demonstrates how an AI engineer builds a system that goes beyond model output by validating, structuring, and preparing data for downstream usage.

---

## 🔹 Input
The workflow accepts a product requirement written in natural language.

Example:
"Users should be able to reset their password using an OTP sent to their registered email..."

---

## 🔹 Output
The system produces three outputs:

1. Structured JSON containing:
   - Feature name
   - Test cases (positive, negative, edge)
   - Edge cases
   - Missing requirements

2. Test Management Payload:
   - Suite name
   - Simplified test cases for execution systems

3. Coverage Summary:
   - Count of positive, negative, and edge cases
   - Missing requirements count

---

## 🔹 Workflow Steps
1. Accept messy product requirement
2. Send input to LLM with strict JSON schema
3. Extract structured test cases
4. Retry extraction if first attempt fails
5. Validate structure and required fields
6. Ensure correct data types and values
7. Generate test-management payload
8. Generate coverage summary

---

## 🔹 Schema Validation
The workflow uses a strict JSON schema (`TEST_CASE_SCHEMA`) to enforce:

- Required fields are present
- Data types are correct
- No extra fields are allowed (`additionalProperties: false`)

### Key Constraints
- `type` must be one of: positive, negative, edge
- `priority` must be one of: low, medium, high
- `steps` must be a list of strings
- Each test case must include:
  - id, title, type, preconditions, steps, expected_result, priority

---

## 🔹 Validation Logic
Additional validation is implemented in code:

- Ensures `test_cases` is a list
- Checks required fields in each test case
- Validates allowed values for `type`
- Ensures `steps` is a list
- Prevents invalid or incomplete outputs

---

## 🔹 Missing Requirements Handling
The system detects unclear or incomplete requirements instead of guessing.

Examples:
- OTP length not specified
- Lock duration not defined
- Retry cooldown not mentioned

---

## 🔹 Test Management Payload
The workflow generates a payload suitable for test execution systems:

- suite_name (feature)
- test_cases with:
  - title
  - priority
  - steps
  - expected_result

---

## 🔹 Coverage Summary
The workflow calculates test coverage:

- Number of positive test cases
- Number of negative test cases
- Number of edge cases
- Count of missing requirements

---

## 🔹 Error Handling
- Retries LLM call if JSON parsing fails
- Handles invalid responses gracefully
- Prevents workflow crashes

---

## 🔹 What Can Go Wrong
- AI may generate incomplete or incorrect test cases
- Some edge cases may be missed
- Incorrect classification of test case type
- API or network failures

---

## 🔹 Future Improvements
- Add retry limits with exponential backoff
- Use Pydantic for stronger validation
- Improve prompt engineering for better accuracy
- Add logging and monitoring
- Integrate with real test management tools (TestRail, Zephyr, etc.)

---

## 🔹 Conclusion
This workflow demonstrates a real AI engineering pattern:

- Converts unstructured requirements into structured test cases
- Validates and enforces schema constraints
- Generates system-ready payloads
- Provides coverage insights

It shows how to build reliable AI-driven systems rather than just using model outputs.