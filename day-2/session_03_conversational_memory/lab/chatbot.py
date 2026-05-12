import os

from common.check_env import check_env
from openai import OpenAI

def main():
    check_env()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", "gpt-5.4-nano")
    messages = []

    print("Chat with the bot (type 'exit' to quit):")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        
        messages.append({"role": "user", "content": user_input})
        
        response = client.responses.create(
            model=model,
            input=messages,
            max_output_tokens=150
        )
        
        assistant_response = response.output_text
        messages.extend([
            {
                "role": "consultant",
                "content": "You are working as a consultant in education assistance firm, speak like a receptionist and answer the question of the user in a polite way."
            },
            {"role": "assistant", "content": assistant_response}
        ])
        print("Bot:", assistant_response)

if __name__ == "__main__":
    main()