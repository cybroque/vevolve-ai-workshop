import streamlit as st
from crew import crew

st.set_page_config(page_title="Finance Roast AI", layout="centered")

st.title("💸 Personal Finance Roast AI 🔥")

st.subheader("Enter your financial details")

income = st.number_input("Monthly Income", min_value=0)
expenses = st.number_input("Monthly Expenses", min_value=0)

if st.button("Generate Roast 🔥"):
    if income == 0 or expenses == 0:
        st.error("Please enter valid values")
    else:
        with st.spinner("Analyzing your financial habits... 💀"):
            result = crew.kickoff(inputs={
                "income": income,
                "expenses": expenses
            })

        st.success("Analysis Complete!")

        st.markdown("## 📊 Finance Report")
        st.write(result.raw)

        # Save file
        with open("outputs/finance_report.md", "w", encoding="utf-8") as f:
            f.write(result.raw)

        st.download_button(
            label="📥 Download Report",
            data=result.raw,
            file_name="finance_report.md",
            mime="text/markdown"
        )