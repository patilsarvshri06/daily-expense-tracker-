
import streamlit as st
import pandas as pd
from datetime import date
import csv
import io

# Page Configuration
st.set_page_config(
    page_title="Daily Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# Initialize Session State
if "transactions" not in st.session_state:
    st.session_state.transactions = []

if "budget" not in st.session_state:
    st.session_state.budget = 10000

# App Title
st.title("💰 Daily Expense Tracker")
st.write("Manage your daily income and expenses easily.")

st.divider()

# Sidebar
st.sidebar.header("⚙️ Settings")

new_budget = st.sidebar.number_input(
    "Set Monthly Budget (₹)",
    min_value=0,
    value=int(st.session_state.budget),
    step=500
)

st.session_state.budget = new_budget

# Add Transaction
st.header("➕ Add New Transaction")

with st.form("transaction_form"):
    col1, col2 = st.columns(2)

    with col1:
        transaction_type = st.selectbox(
            "Transaction Type",
            ["Expense", "Income"]
        )

        amount = st.number_input(
            "Amount (₹)",
            min_value=1,
            step=100
        )

    with col2:
        category = st.selectbox(
            "Category",
            ["Food", "Travel", "Shopping",
             "Education", "Bills", "Health",
             "Salary", "Other"]
        )

        transaction_date = st.date_input(
            "Date",
            value=date.today()
        )

    description = st.text_input("Description")

    submitted = st.form_submit_button(
        "Add Transaction"
    )

    if submitted:
        st.session_state.transactions.append({
            "Type": transaction_type,
            "Amount": amount,
            "Category": category,
            "Date": str(transaction_date),
            "Description": description
        })

        st.success("Transaction added successfully!")
        st.rerun()

st.divider()

# Convert Data into DataFrame
df = pd.DataFrame(st.session_state.transactions)

if not df.empty:

    income = df[df["Type"] == "Income"]["Amount"].sum()

    expenses = df[df["Type"] == "Expense"]["Amount"].sum()

    balance = income - expenses

else:
    income = 0
    expenses = 0
    balance = 0

# Dashboard
st.header("📊 Financial Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Total Income", f"₹{income:,.2f}")
col2.metric("Total Expenses", f"₹{expenses:,.2f}")
col3.metric("Remaining Balance", f"₹{balance:,.2f}")

st.divider()

# Budget Analysis
st.header("🎯 Budget Analysis")

st.write(f"Monthly Budget: ₹{st.session_state.budget:,.2f}")

if st.session_state.budget > 0:

    progress = min(expenses / st.session_state.budget, 1.0)

    st.progress(progress)

    remaining_budget = st.session_state.budget - expenses

    st.write(f"Remaining Budget: ₹{remaining_budget:,.2f}")

    if expenses > st.session_state.budget:
        st.warning("Budget limit exceeded!")

    else:
        st.success("You are within your budget!")

else:
    st.info("Set a budget to see budget analysis.")

st.divider()

# Transaction History
st.header("📋 Transaction History")

if not df.empty:

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # Expense Chart
    st.subheader("📈 Expense by Category")

    expense_df = df[df["Type"] == "Expense"]

    if not expense_df.empty:
        category_data = expense_df.groupby(
            "Category"
        )["Amount"].sum()

        st.bar_chart(category_data)

    # CSV Download
    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Transaction Report",
        data=csv_data,
        file_name="expense_report.csv",
        mime="text/csv"
    )

    # Clear Transactions
    if st.button("🗑️ Clear All Transactions"):
        st.session_state.transactions = []
        st.rerun()

else:
    st.info("No transactions added yet. Start by adding one!")

st.divider()

st.caption("Developed using Python and Streamlit | Daily Expense Tracker")
