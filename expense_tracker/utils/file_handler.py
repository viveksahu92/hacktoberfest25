import pandas as pd
import os

DATA_PATH = "data/expenses.csv"

def load_data():
    if not os.path.exists(DATA_PATH):
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        df = pd.DataFrame(columns=["Date", "Type", "Category", "Amount", "Description"])
        df.to_csv(DATA_PATH, index=False)
    else:
        df = pd.read_csv(DATA_PATH)
    return df

def save_entry(date, entry_type, category, amount, description):
    df = load_data()
    new_entry = pd.DataFrame([[date, entry_type, category, amount, description]],
                             columns=df.columns)
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)
    return df
