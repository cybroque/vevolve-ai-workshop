"""Full tool calling loop: LLM decides to use tool, execute, return result.
Day 4, Session 8: Tool Calling Part B
Learning Objective: Implement 6-step tool calling loop.
"""

import json
import os

from common import get_openai_client


def get_weather(city):
    return f"Weather in {city}: 15°C, cloudy"


def main():
    client = get_openai_client()
    input_items = [{"role": "user", "content": "What is the weather in London?"}]
    tools = [
        {
            "type": "function",
            "name": "get_weather",
            "description": "Get weather for a city",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"],
                "additionalProperties": False,
            },
            "strict": True,
        }
    ]

    # Step 1: LLM call with tools
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
        input=input_items,
        tools=tools,
        max_output_tokens=200,
    )
    # print("Response:", response.output)
    input_items += response.output
    # print("Response:", response.output)
    # Step 2: Check if tool call requested
    for tool_call in response.output:
        if tool_call.type != "function_call":
            continue

        args = json.loads(tool_call.arguments)
        # Step 3: Execute tool
        result = get_weather(args["city"])
        # Step 4: Append tool result to messages
        input_items.append(
            {
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": result,
            }
        )
        print("input_items:", input_items)
        # Step 5: LLM call with tool result
        response2 = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
            input=input_items,
            tools=tools,
            max_output_tokens=200,
        )
        # Step 6: Return final response
        print("Final Response:", response2.output_text)


if __name__ == "__main__":
    main()
