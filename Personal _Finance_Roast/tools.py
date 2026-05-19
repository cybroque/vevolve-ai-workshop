from crewai.tools import BaseTool

class SavingsRateCalculator(BaseTool):
    name: str = "SavingsRateCalculator"
    description: str = "Calculates savings rate and financial health category"

    def _run(self, income: float, expenses: float) -> str:
        if income == 0:
            return "Invalid income"

        savings = income - expenses
        rate = (savings / income) * 100

        if rate < 0:
            category = "Critical"
        elif rate < 10:
            category = "Poor"
        elif rate < 20:
            category = "Fair"
        elif rate < 35:
            category = "Good"
        else:
            category = "Excellent"

        return f"Savings Rate: {rate:.2f}% | Category: {category}"