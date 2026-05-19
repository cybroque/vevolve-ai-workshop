from crew import crew

def main():
    print("\n💸 Personal Finance Roast AI Starting...\n")

    income = float(input("Enter monthly income: "))
    expenses = float(input("Enter total monthly expenses: "))

    inputs = {
        "income": income,
        "expenses": expenses
    }

    result = crew.kickoff(inputs=inputs)

    with open("outputs/finance_report.md", "w", encoding="utf-8") as f:
        f.write(str(result))

    print("\n🔥 Report generated at: outputs/finance_report.md")


if __name__ == "__main__":
    main()