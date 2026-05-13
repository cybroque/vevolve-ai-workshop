---

## 🔹 README Questions

### 1. What input does your workflow accept?
The workflow accepts a messy product requirement written in natural language.  
Example: A description of a feature such as password reset using OTP.

---

### 2. What structured output does it produce?
The workflow produces:
- Structured JSON with feature name, test cases, edge cases, and missing requirements
- A test-management-style payload for execution systems
- A coverage summary showing counts of positive, negative, edge cases, and missing requirements

---

### 3. What validation did you add?
- Ensured required fields are present in the JSON
- Validated that `test_cases` is a list
- Checked that each test case contains required fields (id, title, type, steps, expected_result, priority)
- Enforced allowed values for `type` (positive, negative, edge)
- Ensured `steps` is a list of actions
- Used strict JSON schema with `additionalProperties: false`

---

### 4. What external system could this connect to?
This workflow can integrate with:
- Test management tools (TestRail, Zephyr, Jira Xray)
- CI/CD pipelines for automated testing
- QA dashboards for tracking test coverage

---

### 5. What can go wrong with this workflow?
- AI may generate incomplete or incorrect test cases
- Some edge cases may be missed
- Incorrect classification of test case type
- Invalid or malformed JSON responses
- API/network failures

---

### 6. What would you improve next?
- Add retry limits and better error handling
- Use libraries like Pydantic for stronger validation
- Improve prompt engineering for higher accuracy
- Add logging and monitoring
- Integrate directly with test management tools