"""Async execution and task context dependencies.
Day 4, Session 9: Agents CrewAI Part D
Learning Objective: Run independent tasks in parallel and combine their output.
"""

from crewai import Agent, Crew, Task


def main():

    researcher = Agent(
        role="Researcher",
        goal="Research topics thoroughly",
        backstory="Expert researcher who digs deep into any subject",
    )

    writer = Agent(
        role="Writer",
        goal="Synthesize research into a coherent article",
        backstory="Expert writer who combines multiple sources into clear prose",
    )

    research_trends = Task(
        description="Research the latest trends in AI-assisted coding tools for 2026.",
        expected_output="A bullet list of 3-5 key trends with details.",
        agent=researcher,
        async_execution=True,
    )

    research_risks = Task(
        description="Research the main risks and challenges of AI-assisted coding tools.",
        expected_output="A bullet list of 3-5 key risks with details.",
        agent=researcher,
        async_execution=True,
    )

    write_article = Task(
        description="Write a balanced article covering both the trends and risks of AI coding tools.",
        expected_output="A 3-paragraph article with an introduction, trends section, and risks section.",
        agent=writer,
        context=[research_trends, research_risks],
    )

    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_trends, research_risks, write_article],
        verbose=True,
    )
    result = crew.kickoff()
    print("\n=== Final Article ===")
    print(result)


if __name__ == "__main__":
    main()
