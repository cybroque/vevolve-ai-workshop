# AI-Powered Test Case Generation Workflow

This project converts a natural-language product requirement into structured QA test cases using the OpenAI Responses API with strict JSON Schema enforcement.

The workflow includes:

- AI-based requirement analysis
- structured test case generation
- validation of generated outputs
- test-management payload creation
- coverage analysis

The system is designed to simulate an AI-assisted QA automation pipeline.

---

# Workflow Overview

## Step 1 — Define Requirement

The application starts with a plain-English feature requirement:

```python
requirement = (
    "Users should be able to reset their password using an OTP..."
)