"""Hierarchical crew with a manager LLM.
Day 4, Session 9: Agents CrewAI Part E
Learning Objective: Let a manager LLM delegate tasks to specialist agents.

NOTE: Requires a model with strong function-calling support (e.g. GPT-4o,
Claude 3.5+). Free / weak models often fail to synthesise delegate responses
and may output raw tool calls instead of a final answer.
"""

from crewai import Agent, Crew, Process, Task


def main():

    manager = Agent(
        role="Project Manager",
        goal="Oversee the research project and delegate tasks to specialists",
        backstory="Experienced PM who coordinates research and ensure quality",
        allow_delegation=True,
        max_iter=10,
    )

    specialist = Agent(
        role="Research Specialist",
        goal="Find detailed information on assigned topics",
        backstory="Expert researcher with access to a wide range of knowledge",
    )

    writer = Agent(
        role="Technical Writer",
        goal="Produce well-structured reports from research findings",
        backstory="Experienced technical writer who creates clear, professional reports",
    )

    crew = Crew(
        agents=[specialist, writer],
        tasks=[
            Task(
                description=(
                    "Your job is to write a finished report: get research from the Researcher, "
                    "then write and return the final report. Do NOT ask questions - just write it."
                ),
                expected_output="A complete report with title, 2-3 paragraphs.",
            )
        ],
        process=Process.hierarchical,
        manager_agent=manager,
        verbose=True,
    )
    result = crew.kickoff()
    print("\n=== Hierarchical Crew Output ===")
    print(result)


if __name__ == "__main__":
    main()
