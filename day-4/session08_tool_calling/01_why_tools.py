"""Demo LLM limitations without tools.
Day 4, Session 8: Tool Calling Part A
Learning Objective: Understand why LLMs need external tools.
"""

from common import ask_model


def main():
    print("LLM Response (no tool, likely hallucinates):")
    print(ask_model("What is the current weather in London?", max_output_tokens=100))


if __name__ == "__main__":
    main()
