# README.md: 

##  Workflow

1. **Input:** Receives a raw support message.
2. **AI Processing:** Uses OpenAI to extract key technical details into JSON.
3. **Validation:** Enforces a strict schema to ensure all data (Browser, Steps, etc.) is present.
4. **Payload Generation:** Formats the data into specific templates for Jira and Slack.

---

## Validation Logic

* **Structured Output:** The AI is forbidden from adding extra fields or messy text.
* **No Guessing:** If info is missing, the AI lists it in `missing_information` rather than making it up.
* **Retry Once:** If the first extraction attempt hits an error, the script automatically tries one more time.

##  Potential Failures

* **Missing Key:** The script will fail if the `OPENAI_API_KEY` is not set.
* **Vague Messages:** If the input message is too short (e.g., "It's broken"), the extraction will result in empty fields.
* **Rate Limits:** High-frequency requests may be blocked by the OpenAI API.
