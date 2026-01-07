import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        """
        Create CSV file with headers if it does not exist
        """
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        """
        Add a new transaction entry to CSV
        """
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }

        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)

    @classmethod
    def get_transactions(cls, start_date, end_date):
        """
        Fetch transactions between start_date and end_date
        """
        df = pd.read_csv(cls.CSV_FILE)

        if df.empty:
            return df

        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT)

        start_date = datetime.strptime(start_date, cls.FORMAT)
        end_date = datetime.strptime(end_date, cls.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        return filtered_df


def plot_transactions(df):
    """
    Create income vs expense plot
    """
    if df.empty:
        return None

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)

    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
    )

    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(income_df.index, income_df["amount"], label="Income")
    ax.plot(expense_df.index, expense_df["amount"], label="Expense")

    ax.set_xlabel("Date")
    ax.set_ylabel("Amount")
    ax.set_title("Income vs Expense Over Time")
    ax.legend()
    ax.grid(True)

    return fig
