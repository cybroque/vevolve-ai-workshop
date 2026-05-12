import os
# Note: 'common' is likely a local file provided in your specific workshop
# If you don't have it, you can remove this import and 'check_env()'
from common import check_env 
from openai import OpenAI

def main():
    # Verify environment variables are set
    check_env()
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # "gpt-5.4-nano" is a placeholder; use "gpt-4o-mini" for a working version
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # This list stores the conversation history (the "memory")
    messages = []

    print("Chat with the bot (type 'exit' to quit):")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == "exit":
            break
        
        # Add user's message to history
        messages.append({"role": "user", "content": user_input})
        
        # Standard OpenAI SDK uses client.chat.completions.create
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=150
        )
        
        # Get the text from the response
        assistant_response = response.choices[0].message.content
        
        # Add the AI's reply to history so it "remembers" next time
        messages.append({"role": "assistant", "content": assistant_response})
        
        print(f"Bot: {assistant_response}")

if __name__ == "__main__":
    main()
