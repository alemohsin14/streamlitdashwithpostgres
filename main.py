import calendar
from datetime import datetime
import streamlit as st
import plotly.graph_objects as go

incomes = ["Salary", "Blog"]
expenses = ["Rent", "Car", "Saving"]
currency = "USD"
page_title = "Income and Expense Recorder"

# Page settings
page_icon = ":money_with_wings:"
layout = "centered"

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

# Drop Down Values
years = [datetime.today().year, datetime.today().year + 1]
months = list(calendar.month_name[1:])

# User input
st.header(f"Data Entry in {currency}")
with st.form("enter_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    col1.selectbox("Select Month:", months, key="month")
    col2.selectbox("Select Year:", years, key="year")

    with st.expander("Income"):
        for income in incomes:
            st.number_input(f"{income}:", min_value=0, step=10, key=f"{income}")

    with st.expander("Expenses"):
        for expense in expenses:
            st.number_input(f"{expense}:", min_value=0, step=10, key=f"{expense}")

    with st.expander("Comment"):
        for expense in expenses:
            comment = st.text_area(f"Comment for {expense}:", placeholder=f"Enter a comment for {expense} here..", key=f"comment_{expense}")

    submitted = st.form_submit_button("Save Data")

if submitted:
    period = str(st.session_state["year"]) + " " + str(st.session_state["month"])
    income_data = {income: st.session_state[income] for income in incomes}
    expense_data = {expense: st.session_state[expense] for expense in expenses}
    comments = {expense: st.session_state[f"comment_{expense}"] for expense in expenses}

    st.write(f"Period: {period}")
    st.write(f"Incomes: {income_data}")
    st.write(f"Expenses: {expense_data}")
    st.write(f"Comments: {comments}")
