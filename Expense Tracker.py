"""
Simple Expense Tracker (CLI)
Features:
- Add expense (amount, category, note, date)
- View all expenses
- View summary by category
- View monthly total
- Stores data in 'expenses.json'
"""

import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("expenses.json")

def load_expenses():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_expenses(expenses):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, ensure_ascii=False, indent=2)

def add_expense():
    try:
        amt = float(input("Amount (rupees): ").strip())
    except ValueError:
        print("Galat amount. Dobara try karo.")
        return
    cat = input("Category (e.g., Food, Travel, Bills): ").strip() or "Misc"
    note = input("Note (optional): ").strip()
    date_str = input("Date (YYYY-MM-DD) [leave empty = today]: ").strip()
    if date_str:
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Date format galat. Use YYYY-MM-DD.")
            return
    else:
        date_obj = datetime.today()

    expense = {
        "amount": round(amt, 2),
        "category": cat,
        "note": note,
        "date": date_obj.strftime("%Y-%m-%d")
    }

    expenses = load_expenses()
    expenses.append(expense)
    save_expenses(expenses)
    print("Expense added ✅")

def view_expenses():
    expenses = load_expenses()
    if not expenses:
        print("Koi expense record nahi mila.")
        return
    print("\nAll Expenses:")
    for i, e in enumerate(expenses, 1):
        print(f"{i}. {e['date']} | ₹{e['amount']:.2f} | {e['category']} | {e['note']}")
    print(f"Total items: {len(expenses)}\n")

d
