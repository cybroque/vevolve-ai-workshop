
1. *Bug Report Input*  
   - A messy bug report is given (hard-coded for testing).  

2. *LLM Extraction*  
   - The bug report is converted into a structured JSON object.  
   - JSON Schema is used to enforce required fields.  

3. *Validation*  
   - Rules checked:  
     - steps_to_reproduce must be a list  
     - release_blocker must be a boolean  
     - severity must be one of: low / medium / high  

4. *Jira Payload*  
   - A Jira-style payload is created from the structured bug object.  

5. *Slack Alert*  
   - If release_blocker is true, a Slack alert message is printed.