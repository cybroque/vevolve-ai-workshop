
# 🧠 AI Bug Triage Workflow (Structured Outputs + Automation)

## 📌 Overview

This project is an AI-powered bug triage system that converts messy, natural-language bug reports into structured JSON using OpenAI Structured Outputs.

It then validates the output, generates a Jira-style payload, and optionally sends a Slack-style alert if the bug is a release blocker.

---

# 📥 What input does your workflow accept?

The system accepts **unstructured bug reports written in natural language**.

### Example input:

During regression testing on staging, the login page is not working properly in Chrome.
I entered a valid username and password, clicked the Login button, and the page just kept loading.

Expected result: user should land on the dashboard.  
Actual result: loading spinner stays forever.  

This is blocking our release testing today. Firefox seems to work fine.

# 📤 What structured output does it produce?

The workflow converts the input into a **strict JSON object**:

### Output schema:
- title
- module
- environment
- browser
- severity (low | medium | high | critical)
- release_blocker (boolean)
- steps_to_reproduce (list)
- expected_result
- actual_result
- missing_information
- suggested_next_action

---

# 🧪 What validation did you add?

The system includes a Python validation layer:

### Validations performed:

✔ `steps_to_reproduce` must be a list  
✔ `release_blocker` must be a boolean  
✔ `severity` must be one of:
- low
- medium
- high
- critical  

✔ Ensures required fields exist  
✔ Prevents invalid data from reaching Jira/Slack generation  

---

# 🔗 What external system could this connect to?

This workflow can be integrated with real production tools such as:

### 📌 Jira
- Automatically create bug tickets

### 💬 Slack
- Send alerts for release blockers

### 📊 Test management tools
- Xray
- TestRail

### 📡 DevOps pipelines
- CI/CD systems (GitHub Actions, Jenkins)

---

# ⚠️ What can go wrong with this workflow?

Even with structured outputs, several issues may occur:

### 1. Invalid AI output
- JSON parsing failure
- malformed response

### 2. Missing or incorrect data
- AI may omit fields
- incorrect severity classification

### 3. Hallucinated information
- AI may guess missing details (if not controlled properly)

### 4. Downstream integration failures
- Jira/Slack API errors
- authentication issues

### 5. Over-alerting
- too many Slack notifications if release_blocker logic is not strict

---

# 🚀 What would you improve next?

Future improvements could include:

### 🔥 1. Real API integrations
- Jira REST API ticket creation
- Slack webhook integration

### 🔥 2. Retry + error handling system
- handle API failures gracefully

### 🔥 3. Logging system
- store all bug reports and outputs

### 🔥 4. Database storage
- PostgreSQL / MongoDB for tracking bugs

### 🔥 5. Web dashboard
- visualize bugs and severity levels

### 🔥 6. Multi-agent AI system
- separate agents for:
  - triage
  - validation
  - prioritization

---

# 🧠 Summary

This project demonstrates a real-world AI engineering workflow that:

> Converts unstructured bug reports → structured JSON → validated → actionable Jira/Slack outputs

It is a foundation for building production-grade AI QA automation systems.