import psycopg2
import streamlit as st
from datetime import datetime
import plotly.express as px

# Define database connection parameters
db_params = {
    'host': 'localhost',
    'database': 'test_db',
    'user': 'postgres',
    'password': '1234',
    'port': 5434
}

# Establish a connection to the database
conn = psycopg2.connect(**db_params)

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Streamlit app settings
st.set_page_config(
    page_title="Income and Expense Recorder",
    page_icon=":money_with_wings:",
    layout="wide"
)

st.title("Income and Expense Recorder :money_with_wings:")

# User input
st.header("Data Entry")
with st.form("enter_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    selected_month = col1.selectbox("Select Month:", range(1, 13), index=datetime.today().month - 1)
    selected_year = col2.selectbox("Select Year:", range(2000, datetime.today().year + 1), index=0)

    with st.expander("Income"):
        incomes = {}
        for source in ["Salary", "Blog"]:
            incomes[source] = col1.number_input(f"{source}:", min_value=0, step=10, key=source)

    with st.expander("Expenses"):
        expenses = {}
        for expense in ["Rent", "Car", "Saving"]:
            expenses[expense] = col2.number_input(f"{expense}:", min_value=0, step=10, key=expense)

    # Add a submit button inside the form
    submit_button = st.form_submit_button("Submit")

# Check if the form was submitted
if submit_button:
    # Calculate balance
    total_income = sum(incomes.values())
    total_expense = sum(expenses.values())
    balance = total_income - total_expense

    # Insert data into the database
    try:
        cursor.execute(
            "INSERT INTO income_expense (month, year, total_income, total_expense, balance) VALUES (%s, %s, %s, %s, %s)",
            (selected_month, selected_year, total_income, total_expense, balance)
        )
        conn.commit()
        st.success("Data saved successfully!")
    except psycopg2.Error as e:
        conn.rollback()
        st.error(f"Error: {e}")

# Data Visualization
st.header("Data Visualization")

# Retrieve data from the database
try:
    cursor.execute("SELECT * FROM income_expense")
    data = cursor.fetchall()
except psycopg2.Error as e:
    st.error(f"Error fetching data: {e}")
else:
    if data:
        # Create a DataFrame from the data
        import pandas as pd
        df = pd.DataFrame(data, columns=["id", "month", "year", "total_income", "total_expense", "balance", "created_at"])

        # Create a line chart to visualize the balance over time
        fig = px.line(df, x="created_at", y="balance", title="Balance Over Time")
        st.plotly_chart(fig)
    else:
        st.warning("No data available for visualization.")

# Close the cursor and the database connection
cursor.close()
conn.close()
