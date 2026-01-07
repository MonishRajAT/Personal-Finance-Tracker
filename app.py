import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
from main import CSV

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Personal Finance Tracker",
    layout="centered"
)

CSV.initialize_csv()

# ---------------- Sidebar ----------------
menu = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "➕ Add Transaction", "📄 View Transactions", "📊 Visualize Transactions"]
)


# HOME PAGE

if menu == "🏠 Home":
    st.title("💰 Personal Finance Tracker")

    with st.spinner("Loading application..."):
        time.sleep(0.6)

    st.success("Application ready ✅")

    st.markdown("""
    ### 📌 About This App
    This Personal Finance Tracker helps you **record, track, and analyze**
    your daily **income and expenses** efficiently.

    ### ⚙️ How It Works
    - Add income or expense transactions  
    - View transactions within a date range  
    - Analyze finances using monthly insights and charts  

    ### 🚀 Features
    - CSV-based persistent storage  
    - Income & Expense categorization  
    - Date and month-wise filtering  
    - Interactive visual analytics  
    """)

    st.info("💡 Tip: Monthly analysis helps you control unnecessary expenses")

#ADD TRANSACTION

elif menu == "➕ Add Transaction":
    st.title("➕ Add New Transaction")

    date = st.date_input("Transaction Date")
    amount = st.number_input("Amount", min_value=1.0, step=1.0)
    category = st.selectbox("Category", ["Income", "Expense"])
    description = st.text_input("Description (optional)")

    if st.button("Add Transaction"):
        with st.status("Saving transaction...", expanded=False):
            time.sleep(0.4)
            CSV.add_entry(
                date.strftime("%d-%m-%Y"),
                amount,
                category,
                description
            )
            time.sleep(0.3)

        st.toast("Transaction added successfully 💾", icon="✅")

#VIEW TRANSACTIONS

elif menu == "📄 View Transactions":
    st.title("📄 View Transactions")

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Start Date")
    with col2:
        end_date = st.date_input("End Date")

    if st.button("Show Transactions"):
        with st.spinner("Fetching transactions..."):
            time.sleep(0.6)
            df = CSV.get_transactions(
                start_date.strftime("%d-%m-%Y"),
                end_date.strftime("%d-%m-%Y")
            )

        if df.empty:
            st.warning("No transactions found for the selected date range.")
        else:
            st.dataframe(df, use_container_width=True)

            total_income = df[df["category"] == "Income"]["amount"].sum()
            total_expense = df[df["category"] == "Expense"]["amount"].sum()
            net_savings = total_income - total_expense

            st.subheader("📌 Summary")

            c1, c2, c3 = st.columns(3)
            c1.metric("Total Income", f"₹ {total_income:.2f}")
            c2.metric("Total Expense", f"₹ {total_expense:.2f}")
            c3.metric("Net Savings", f"₹ {net_savings:.2f}")


#VISUALIZE TRANSACTIONS (MONTHLY ANALYSIS)

elif menu == "📊 Visualize Transactions":
    st.title("📊 Monthly Financial Analysis")

    df_all = pd.read_csv(CSV.CSV_FILE)

    if df_all.empty:
        st.warning("No data available. Please add transactions first.")
    else:
        df_all["date"] = pd.to_datetime(df_all["date"], format="%d-%m-%Y")
        df_all["Year-Month"] = df_all["date"].dt.to_period("M").astype(str)

        # -------- Monthly Dropdown --------
        selected_month = st.selectbox(
            "Select Month",
            sorted(df_all["Year-Month"].unique(), reverse=True)
        )

        with st.spinner("Preparing monthly analysis..."):
            time.sleep(0.5)

        monthly_df = df_all[df_all["Year-Month"] == selected_month]

        total_income = monthly_df[monthly_df["category"] == "Income"]["amount"].sum()
        total_expense = monthly_df[monthly_df["category"] == "Expense"]["amount"].sum()
        net_savings = total_income - total_expense

        # -------- Metrics --------
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Income", f"₹ {total_income:.2f}")
        c2.metric("Total Expense", f"₹ {total_expense:.2f}")
        c3.metric("Net Savings", f"₹ {net_savings:.2f}")

        # -------- Monthly Plot --------
        monthly_df.set_index("date", inplace=True)

        income_df = monthly_df[monthly_df["category"] == "Income"].resample("D").sum()
        expense_df = monthly_df[monthly_df["category"] == "Expense"].resample("D").sum()

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(income_df.index, income_df["amount"], label="Income")
        ax.plot(expense_df.index, expense_df["amount"], label="Expense")

        ax.set_title(f"Income vs Expense – {selected_month}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Amount")
        ax.legend()
        ax.grid(True)
        fig.autofmt_xdate(rotation=45)

        st.pyplot(fig)

        st.toast("Monthly analysis ready 📊", icon="📈")
