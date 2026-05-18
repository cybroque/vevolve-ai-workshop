import os
import sys
from crewai_tools import SerperDevTool
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from crewai import Agent, Crew, Task


def main():
    search_tool = SerperDevTool()
    bug_reader = Agent(
        role="Bug Reader",
        goal="Extract key details from bug reports",
        backstory="Expert in analyzing bug reports and summarizing key information",
        tools=[search_tool]
    )
    triage_analyst = Agent(
        role="Triage Analyst",
        goal="Classify and prioritize bugs based on severity and impact",
        backstory="Experienced software engineer who understands bug triage and prioritization",
        tools=[search_tool]
    )
    test_case_generator = Agent(
        role="Test Case Generator",
        goal="Generate regression test cases for reported bugs",
        backstory="Automation testing expert who can create effective test cases based on bug details",
        tools=[search_tool]
    )
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
        expected_output="Structured summary of the bug report with key details.",
        agent=bug_reader,
    )
    task2 = Task(
        description="""
        Analyze the extracted bug details and classify:
        - Severity
        - Priority
        - Affected component
        """,
        expected_output="Bug triage report with severity, priority, and component.",
        agent=triage_analyst,
    )
    task3 = Task(
        description="Generate regression test cases for the reported login issue.",
        expected_output="2-3 regression test cases for login functionality.",
        agent=test_case_generator,
    )
    crew = Crew(agents=[bug_reader, triage_analyst, test_case_generator], tasks=[task1, task2, task3], verbose=True)
    result = crew.kickoff()
    print("Crew Result:", result)

if __name__ == "__main__":
    main()