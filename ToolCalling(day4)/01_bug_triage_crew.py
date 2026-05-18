from crewai import Agent, Crew, Task


def main():

    Bug_Reader = Agent(
        role="Bug Report Analyst",
        goal=(
            "Analyze incoming bug reports and extract all important "
            "details such as issue summary, environment, steps to reproduce, "
            "expected behavior, and actual behavior."
        ),
        backstory=(
            "You are an experienced QA analyst with strong expertise in "
            "understanding software defect reports. You are skilled at "
            "identifying missing information, organizing bug details clearly, "
            "and preparing reports for further triage."
        ),
        verbose=True,
    )

    Triage_Analyst = Agent(
        role="Bug Triage Analyst",
        goal=(
            "Classify bugs based on severity, priority, affected component, "
            "and business impact to help development teams resolve issues efficiently."
        ),
        backstory=(
            "You are a senior triage engineer who has worked with multiple "
            "software teams handling production and testing defects. "
            "You specialize in identifying the impact of bugs and assigning "
            "the correct severity and ownership."
        ),
        verbose=True,
    )

    Test_case_generator = Agent(
        role="Test Case Generator",
        goal=(
            "Generate detailed functional and edge-case test cases "
            "based on the analyzed bug report."
        ),
        backstory=(
            "You are an automation testing expert with deep knowledge of "
            "software validation techniques. You create high-quality test "
            "scenarios that help QA teams reproduce issues and prevent regressions."
        ),
        verbose=True,
    )

    task1 = Task(
        description=(
            "Read the provided bug report carefully and extract all key details. "
            "Identify the issue summary, steps to reproduce, expected result, "
            "actual result, affected environment, and any missing information."
        ),
        expected_output=(
            "A structured bug analysis report containing:\n"
            "- Bug Summary\n"
            "- Environment Details\n"
            "- Steps to Reproduce\n"
            "- Expected Behavior\n"
            "- Actual Behavior\n"
            "- Additional Observations"
        ),
        agent=Bug_Reader,
    )

    task2 = Task(
        description=(
            "Analyze the extracted bug details and classify the bug based on "
            "severity, priority, impacted module/component, and business impact."
        ),
        expected_output=(
            "A triage report containing:\n"
            "- Severity Level\n"
            "- Priority Level\n"
            "- Affected Component\n"
            "- Root Cause Assumption\n"
            "- Business Impact\n"
            "- Recommended Team Assignment"
        ),
        agent=Triage_Analyst,
    )

    task3 = Task(
        description=(
            "Generate comprehensive test cases based on the analyzed bug report "
            "to validate the issue and prevent future regressions."
        ),
        expected_output=(
            "A detailed set of test cases including:\n"
            "- Positive Test Scenarios\n"
            "- Negative Test Scenarios\n"
            "- Edge Cases\n"
            "- Preconditions\n"
            "- Test Steps\n"
            "- Expected Results"
        ),
        agent=Test_case_generator,
    )
    crew = Crew(
        agents=[Bug_Reader, Triage_Analyst, Test_case_generator],
        tasks=[task1, task2, task3],
        verbose=True,
    )
    result = crew.kickoff()

    print("\n\n########################")
    print("## Crew Result:")
    print("########################\n")
    print(result)


if __name__ == "__main__":
    main()