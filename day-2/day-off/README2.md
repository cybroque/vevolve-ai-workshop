# AI-Powered Structured Test Case Generator

## Overview
This project converts a plain-language software requirement into structured QA test cases using the OpenAI Responses API with JSON Schema validation.

The workflow:
1. Accepts a requirement as input.
2. Sends the requirement to an OpenAI model.
3. Forces the model to return structured JSON using a strict schema.
4. Validates the generated output.
5. Converts the result into a test-management payload.
6. Generates a coverage summary.

---

