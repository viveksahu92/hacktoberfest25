import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.file_handler import load_data, save_entry
from utils.calculations import get_summary, get_category_summary

st.set_page_config(page_title="Expense Tracker", layout="wide")

st.title(" Personal Expense Tracker")

tab1, tab2, tab3 = st.tabs([" Add Entry", " View Transaction", "Summary"])


with tab1:
    st.subheader("Add a New Transaction")

    col1, col2, col3 = st.columns(3)
    with col1:
        date = st.date_input("Date")
    with col2:
        entry_type = st.selectbox("Type", ["Income", "Expense"])
    with col3:
        category = st.text_input("Category")

    amount = st.number_input("Amount", min_value=0.0, step=0.1)
    description = st.text_area("Description")

    if st.button(" Save Entry"):
        if category and amount > 0:
            save_entry(str(date), entry_type, category, amount, description)
            st.success("Entry added successfully!")
        else:
            st.error("Please enter valid category and amount.")


with tab2:
    st.subheader("All Transactions")
    df = load_data()
    st.dataframe(df, use_container_width=True)


with tab3:
    st.subheader("Financial Overview")

    df = load_data()
    income, expense, balance = get_summary(df)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"₹ {income:,.2f}")
    col2.metric("Total Expense", f"₹ {expense:,.2f}")
    col3.metric("Balance", f"₹ {balance:,.2f}")

    # Category chart
    cat_summary = get_category_summary(df)
    if not cat_summary.empty:
        fig, ax = plt.subplots(figsize=(8, 4))
        for t in ["Income", "Expense"]:
            sub = cat_summary[cat_summary["Type"] == t]
            ax.bar(sub["Category"], sub["Amount"], label=t)
        ax.set_title("Category-wise Breakdown")
        ax.set_xlabel("Category")
        ax.set_ylabel("Amount")
        ax.legend()
        st.pyplot(fig)
    else:
        st.info("No data to display yet.")
