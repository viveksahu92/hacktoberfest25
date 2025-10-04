import pandas as pd

def get_summary(df):
    income = df[df["Type"] == "Income"]["Amount"].sum()
    expense = df[df["Type"] == "Expense"]["Amount"].sum()
    balance = income - expense
    return income, expense, balance

def get_category_summary(df):
    return df.groupby(["Type", "Category"])["Amount"].sum().reset_index()
