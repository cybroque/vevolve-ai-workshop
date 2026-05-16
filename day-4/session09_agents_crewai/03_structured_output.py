"""Structured output with Pydantic models.
Day 4, Session 9: Agents CrewAI Part C
Learning Objective: Get typed, validated outputs from agents using Pydantic.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from crewai import Agent, Crew, Task
from pydantic import BaseModel


class ResearchFinding(BaseModel):
    trend: str
    impact: str
    confidence: str


class ResearchReport(BaseModel):
    topic: str
    findings: list[ResearchFinding]
    summary: str


def main():

    researcher = Agent(
        role="Researcher",
        goal="Research a topic and produce structured findings",
        backstory="Expert at distilling complex topics into structured data",
    )

    research = Task(
        description="Research the current state of agentic AI workflows.",
        expected_output="A structured report with findings and a summary.",
        agent=researcher,
        output_pydantic=ResearchReport,
    )

    crew = Crew(agents=[researcher], tasks=[research], verbose=True)
    result = crew.kickoff()

    print("\n=== Structured Output ===")
    print(result)

    print("\n=== Access via Pydantic ===")
    report: ResearchReport = result.pydantic
    print(f"Topic: {report.topic}")
    for f in report.findings:
        print(f"  - {f.trend} ({f.confidence}): {f.impact}")
    print(f"Summary: {report.summary}")


if __name__ == "__main__":
    main()
