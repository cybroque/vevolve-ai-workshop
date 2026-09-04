import os
import dotenv
import openai

def load_env():
    """Load environment variables from .env file. Returns True if successful."""
    dotenv.load_dotenv()
    return os.path.exists(".env")

def main():

    #check_env()
    load_env()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file")
  
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", "gpt-5.4-nano")
    messages = []

    

    user_input = input("Set BOT Role: ")
    messages.append({"role": "system", "content": "act as "+user_input})

    print("Chat with --"+user_input+"-- (type 'exit' to quit:)")

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

        messages.append({
            "role": "assistant",
            "content": assistant_response
        })

        print("Bot:", assistant_response)


if __name__ == "__main__":
    main()