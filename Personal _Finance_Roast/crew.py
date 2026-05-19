from crewai import Agent, Task, Crew, Process
from tools import SavingsRateCalculator
from dotenv import load_dotenv
import os

load_dotenv()

# ---------------- AGENTS ---------------- #

expense_auditor = Agent(
    role="Expense Auditor",
    goal="Analyze income and expenses and categorize spending",
    backstory="You are a strict financial analyst who finds wasteful spending.",
    tools=[SavingsRateCalculator()],
    verbose=True
)

roast_agent = Agent(
    role="Roast Agent",
    goal="Give brutally honest financial roast",
    backstory="You are a savage financial coach who never sugarcoats anything.",
    verbose=True
)

savings_planner = Agent(
    role="Savings Planner",
    goal="Create a realistic savings plan",
    backstory="You are a disciplined financial planner focused on growth.",
    verbose=True
)

# ---------------- TASKS ---------------- #

audit_task = Task(
    description="""
Analyze income and expenses.
Break down spending categories and identify wasteful habits.
""",
    expected_output="Expense breakdown with insights",
    agent=expense_auditor
)

roast_task = Task(
    description="""
Based on the audit, roast the user's spending habits brutally but humorously.
""",
    expected_output="Roast report",
    agent=roast_agent
)

saving_task = Task(
    description="""
Create a 3-month savings plan based on spending behavior.
""",
    expected_output="Savings strategy",
    agent=savings_planner
)

# ---------------- CREW ---------------- #

crew = Crew(
    agents=[expense_auditor, roast_agent, savings_planner],
    tasks=[audit_task, roast_task, saving_task],
    process=Process.sequential,
    verbose=True
)