import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
)

from crewai import Agent, Crew, Task


def main():

    # Create Agent
    bug_reader = Agent(
        role="Bug Reader",
        goal="Extract key details from bug reports",
        backstory="Expert in analyzing and summarizing software bug reports",
        verbose=True
    )

    # Create Single Task
    task1 = Task(
        description="""
        Read the following bug report and extract:

        - Bug summary
        - Steps to reproduce
        - Expected behavior
        - Actual behavior

        Bug Report:
        Login button crashes the app when user enters invalid credentials.
        """,
        expected_output="Structured bug report summary.",
        agent=bug_reader,
    )

    # Create Crew
    crew = Crew(
        agents=[bug_reader],
        tasks=[task1],
        verbose=True
    )

    # Run Crew
    result = crew.kickoff()

    print("\nFinal Result:\n")
    print(result)


if __name__ == "__main__":
    main()