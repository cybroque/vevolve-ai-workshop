
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from crewai import Agent, Crew, Task

# # uv add crewai


def main():

    researcher = Agent(
        role="Researcher", goal="Research topic", backstory="Expert researcher"
    )
    writer = Agent(role="Writer", goal="Write article", backstory="Expert writer")

    task1 = Task(
        description="Research AI trends",
        expected_output="A concise bullet list of 3-5 AI trends with one sentence per trend.",
        agent=researcher,
    )
    task2 = Task(
        description="Write an article on AI trends using the research summary.",
        expected_output="A short article with a title and 2-3 paragraphs.",
        agent=writer,
    )
    reviewer = Agent(
        role="Reviewer",
        goal="Review and improve the article",
        backstory="Expert editor who checks grammar, clarity, and accuracy",
    )

    task3 = Task(
        description="Review and improve the article.",
        expected_output="A polished article with improved grammar, clarity, and accuracy.",
        agent=reviewer,
    )

    crew = Crew(agents=[researcher, writer, reviewer], tasks=[task1, task2, task3], verbose=True)
    result = crew.kickoff()
    print("Crew Result:", result)


if __name__ == "__main__":
    main()