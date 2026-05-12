"""
Chatbot that uses conversational memory to maintain context and provide relevant responses.
"""
import os

from test import check_env
from openai import OpenAI

def main():
    # Ensure environment variables are loaded
    check_env()
    
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Model selection (defaulting to gpt-5.4-nano)
    model = os.getenv("OPENAI_MODEL", "gpt-5.4-nano")
    messages = []

    print("Chatbot is ready! Type 'exit' to quit.")
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
            max_output_tokens=150
        )
        
        # Access response text directly
        assistant_response = response.output_text
        
        # Update history with the assistant's reply
        messages.append({"role": "assistant", "content": assistant_response})
        
        print("Bot:", assistant_response)

if __name__ == "__main__":
    main()