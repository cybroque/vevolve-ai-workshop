"""Define tool schemas using JSON Schema.
Day 4, Session 8: Tool Calling Part C
Learning Objective: Write valid JSON schemas for tools.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))


def main():
    tool_schema = {
        "type": "function",
        "name": "get_os_info",
        "description": "Get operating system information",
        "parameters": {
            "type": "object",
            "properties": {
                "os_name": {"type": "string", "enum": ["Windows", "Linux", "macOS"]}
            },
            "required": ["os_name"],
            "additionalProperties": False
        },
        "strict": True
    }
    print("Tool Schema:")
    print(tool_schema)


if __name__ == "__main__":
    main()
