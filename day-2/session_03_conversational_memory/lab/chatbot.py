"""
Chatbot that uses conversational memory to maintain context and provide relevant responses.
"""
import os
from common import check_env
from openai import OpenAI

def main():
    # Ensure environment variables are loaded
    check_env()
    
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Model selection (defaulting to gpt-5.4-nano)
    model = os.getenv("OPENAI_MODEL", "gpt-5.4-nano")
    rtf_prompt = """
Role: You are a senior QA engineer.
Task: Write Testcases for the system
Format: Problem,solution,suggestion
"""
    
    messages = [{"role": "system", "content": "You are QA tester, Replay like that"},{"role": "system", "content": rtf_prompt}]

    print("Chat with the bot (type 'exit' to quit):")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == "exit":
            break
        
        # Append user message to the conversation history
        messages.append({"role": "user", "content": user_input})
        
        # Modern Responses API call
        response = client.responses.create(
            model=model, 
            input=messages, 
            max_output_tokens=150,
            temperature=0.7
        )
        
        # Access response text directly
        assistant_response = response.output_text
        
        # Update history with the assistant's reply
        messages.append({"role": "assistant", "content": assistant_response})
        
        print("Bot:", assistant_response)

if __name__ == "__main__":
    main()