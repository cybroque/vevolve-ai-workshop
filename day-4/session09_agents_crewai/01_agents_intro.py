"""Single CrewAI agent with tools.
Day 4, Session 9: Agents CrewAI Part A
Learning Objective: Define a CrewAI agent with a tool.
"""

from crewai import Agent


def main():
    agent = Agent(
        role="Researcher",
        goal="Research AI trends",
        backstory="Expert in AI and machine learning",
        verbose=True,
    )
    print("Agent created:", agent.role)


if __name__ == "__main__":
    main()
