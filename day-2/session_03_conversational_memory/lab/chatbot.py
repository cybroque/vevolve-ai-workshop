import os
import dotenv
import openai
def load_env():
    dotenv.load_dotenv()
    return os.path.exists('.env')
def main():
    load_env()
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    model = os.getenv('OPENAI_MODEL', 'gpt-5.4-nano')
    messages = []
    print("Welcome to the AI Chatbot! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        messages.append({"role": "user", "content": user_input})
        response = client.responses.create(model=model, input=messages,max_output_tokens=150)
        assistant_response = response.output_text
        messages.append({"role": "assistant", "content": assistant_response})   
        print(f"AI: {assistant_response}")

if __name__ == "__main__":
    main()
