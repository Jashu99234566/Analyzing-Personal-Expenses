import mysql.connector
import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

# MySQL connection details
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Jashu@123",
        database="ExpenseDB"
    )

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Query Visualizations"])

# Home Page
if page == "Home":
    st.title("Expense Data Dashboard")
    st.write("""
    This dashboard provides insights into the expense data generated using Faker and stored in MySQL.
    
    Navigate to **Query Visualizations** to view specific queries and their corresponding charts.
    """)

# Query Visualizations Page
elif page == "Query Visualizations":
    st.title("Query Visualizations")

    # Establishing connection
    conn = get_connection()
    cursor = conn.cursor()

    # Query 1: Total expenses by category
    cursor.execute("SELECT Category, SUM(Amount) AS Total_Amount FROM Expenses GROUP BY Category;")
    result1 = cursor.fetchall()
    df1 = pd.DataFrame(result1, columns=['Category', 'Total Amount'])
    st.subheader("1. Total Expenses by Category")
    fig = px.bar(
    df1, 
    x='Category', 
    y='Total Amount', 
    title='Total Expenses by Category',
    labels={'Category': 'Expense Category', 'Total Amount': 'Total Amount Spent'},
    color='Total Amount',
    color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig)    

    # Query 2: Monthly total expenses
    cursor.execute("SELECT DATE_FORMAT(Date, '%Y-%m') AS Month, SUM(Amount) AS Total_Amount FROM Expenses GROUP BY Month;")
    result2 = cursor.fetchall()
    df2 = pd.DataFrame(result2, columns=['Month', 'Total Amount'])
    st.subheader("2. Monthly Total Expenses")
    fig2 = px.line(df2, x='Month', y='Total Amount', title='Monthly Total Expenses')
    st.plotly_chart(fig2)

    # Query 3: Top 5 most expensive transactions
    cursor.execute("SELECT * FROM Expenses ORDER BY Amount DESC LIMIT 5;")
    result3 = cursor.fetchall()
    df3 = pd.DataFrame(result3, columns=['ID', 'Date', 'Category', 'Payment Mode', 'Description', 'Amount'])
    st.subheader("3. Top 5 Most Expensive Transactions")
    st.table(df3)

    # Query 4: Average expense per category
    cursor.execute("SELECT Category, AVG(Amount) AS Average_Amount FROM Expenses GROUP BY Category;")
    result4 = cursor.fetchall()
    df4 = pd.DataFrame(result4, columns=['Category', 'Average Amount'])
    st.subheader("4. Average Expense per Category")
    fig = px.pie(df4, values='Average Amount', names='Category', title='Average Expense per Category')
    st.plotly_chart(fig)

    # Query 5: Total expenses by payment mode
    cursor.execute("SELECT Payment_Mode, SUM(Amount) AS Total_Amount FROM Expenses GROUP BY Payment_Mode;")
    result5 = cursor.fetchall()
    df5 = pd.DataFrame(result5, columns=['Payment Mode', 'Total Amount'])
    st.subheader("5. Total Expenses by Payment Mode")
    fig = px.bar(df5, x='Total Amount', y='Payment Mode', orientation='h', title='Total Expenses by Payment Mode', color='Payment Mode')
    st.plotly_chart(fig)

    # Query 6: Number of transactions by category
    cursor.execute("SELECT Category, COUNT(*) AS Transactions FROM Expenses GROUP BY Category;")
    result6 = cursor.fetchall()
    df6 = pd.DataFrame(result6, columns=['Category', 'Number of Transactions'])
    st.subheader("6. Number of Transactions by Category")
    st.bar_chart(df6.set_index('Category'))

    # Query 7: Highest expense per month
    cursor.execute("SELECT DATE_FORMAT(Date, '%Y-%m') AS Month, MAX(Amount) AS Max_Amount FROM Expenses GROUP BY Month;")
    result7 = cursor.fetchall()
    df7 = pd.DataFrame(result7, columns=['Month', 'Max Amount'])
    st.subheader("7. Highest Expense per Month")
    st.line_chart(df7.set_index('Month'))

    # Query 8: Minimum expense per category
    cursor.execute("SELECT Category, MIN(Amount) AS Min_Amount FROM Expenses GROUP BY Category;")
    result8 = cursor.fetchall()
    df8 = pd.DataFrame(result8, columns=['Category', 'Min Amount'])
    st.subheader("8. Minimum Expense per Category")
    st.table(df8)

    # Query 9: Total expenses for the year
    cursor.execute("SELECT SUM(Amount) AS Total_Expense FROM Expenses;")
    result9 = cursor.fetchone()
    st.subheader("9. Total Expenses for the Year")
    st.metric("Total Expense", f"₹{result9[0]:,.2f}")

    # Query 10: Category with highest total expense
    cursor.execute("SELECT Category, SUM(Amount) AS Total_Amount FROM Expenses GROUP BY Category ORDER BY Total_Amount DESC LIMIT 1;")
    result10 = cursor.fetchone()
    st.subheader("10. Category with Highest Total Expense")
    st.write(f"The category with the highest total expense is **{result10[0]}** with a total of **₹{result10[1]:,.2f}**.")

    # Query 11: Payment mode with most transactions
    cursor.execute("SELECT Payment_Mode, COUNT(*) AS Transactions FROM Expenses GROUP BY Payment_Mode ORDER BY Transactions DESC LIMIT 1;")
    result11 = cursor.fetchone()
    st.subheader("11. Payment Mode with Most Transactions")
    st.write(f"The payment mode used most frequently is **{result11[0]}** with **{result11[1]}** transactions.")

    # 12. Find the Category with the Lowest Spending
    query12 = "SELECT Category, SUM(Amount) AS Total_Spent FROM Expenses GROUP BY Category ORDER BY Total_Spent ASC LIMIT 1;"
    cursor.execute(query12)
    result12 = cursor.fetchall()
    df12 = pd.DataFrame(result12, columns=['Category', 'Total Spent'])
    st.subheader("12. Category with the Lowest Spending")
    st.write(df12)  # Display table since it's a single row

    # 13. Total Spending by Quarter
    query13 = "SELECT QUARTER(Date) AS Quarter, SUM(Amount) AS Total_Spent FROM Expenses GROUP BY Quarter ORDER BY Quarter;"
    cursor.execute(query13)
    result13 = cursor.fetchall()
    df13 = pd.DataFrame(result13, columns=['Quarter', 'Total Spent'])
    st.subheader("13. Total Spending by Quarter")
    chart13 = alt.Chart(df13).mark_bar().encode(
    x=alt.X('Quarter:O', title='Quarter'),
    y=alt.Y('Total Spent:Q', title='Total Spent'),
    color='Quarter:O'
    ).properties(title='Total Spending by Quarter')
    st.altair_chart(chart13, use_container_width=True)

    # 14. Identify the Most Common Description
    query14 = "SELECT Description, COUNT(*) AS Occurrences FROM Expenses GROUP BY Description ORDER BY Occurrences DESC LIMIT 1;"
    cursor.execute(query14)
    result14 = cursor.fetchall()
    df14 = pd.DataFrame(result14, columns=['Description', 'Occurrences'])
    st.subheader("14. Most Common Description")
    st.write(df14)  # Display as table for a single result

    # 15. Spending Comparison: Cash vs Credit Card
    query15 = "SELECT Payment_Mode, SUM(Amount) AS Total_Spent FROM Expenses WHERE Payment_Mode IN ('Cash', 'Credit Card') GROUP BY Payment_Mode;"
    cursor.execute(query15)
    result15 = cursor.fetchall()
    df15 = pd.DataFrame(result15, columns=['Payment Mode', 'Total Spent'])
    st.subheader("15. Spending Comparison (Cash vs Credit Card)")
    chart15 = alt.Chart(df15).mark_bar().encode(
    x=alt.X('Payment Mode:O', title='Payment Mode'),
    y=alt.Y('Total Spent:Q', title='Total Spent'),
    color='Payment Mode:O'
    ).properties(title='Spending Comparison: Cash vs Credit Card')
    st.altair_chart(chart15, use_container_width=True)

    # 16. Identify the Least Used Payment Mode
    query16 = "SELECT Payment_Mode, COUNT(*) AS Usage_Count FROM Expenses GROUP BY Payment_Mode ORDER BY Usage_Count ASC LIMIT 1;"
    cursor.execute(query16)
    result16 = cursor.fetchall()
    df16 = pd.DataFrame(result16, columns=['Payment Mode', 'Usage Count'])
    st.subheader("16. Least Used Payment Mode")
    st.write(df16)  # Display as table for a single result

    # 17. Monthly Spending in the 'Travel' Category
    query17 = "SELECT DATE_FORMAT(Date, '%Y-%m') AS Month, SUM(Amount) AS Total_Spent FROM Expenses WHERE Category = 'Travel' GROUP BY Month ORDER BY Month;"
    cursor.execute(query17)
    result17 = cursor.fetchall()
    df17 = pd.DataFrame(result17, columns=['Month', 'Total Spent'])
    st.subheader("17. Monthly Spending in the 'Travel' Category")
    chart17 = alt.Chart(df17).mark_line(point=True).encode(
    x=alt.X('Month:T', title='Month'),
    y=alt.Y('Total Spent:Q', title='Total Spent'),
    tooltip=['Month:T', 'Total Spent:Q']
        ).properties(title='Monthly Spending in the Travel Category')
    st.altair_chart(chart17, use_container_width=True)
