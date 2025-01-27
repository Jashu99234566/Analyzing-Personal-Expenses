import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt
import streamlit as st
import pymysql 

# Define a function to connect to the MySQL database
def get_connection():
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="Jashu@#1234",  # Replace with your MySQL password
            database="ExpenseDB"  # Replace with your database name
        )
        return connection
    except pymysql.Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

# Sidebar navigation
st.sidebar.title("Expense Analysis")
page = st.sidebar.radio("Go to", ["Home", "Query Visualizations"])
# Home Page
if page == "Home":
    st.title("Welcome to the Expense Analysis Dashboard")
    st.write("""
    This dashboard answers key questions about your spending habits by running SQL queries on expense data stored in a MySQL database. Use the sidebar to navigate to the Query Visualizations page and explore interactive charts and insights.
    """)

# Query Visualizations Page
elif page == "Query Visualizations":
    st.title("Query Visualizations")

# Establish connection
    conn = get_connection()
    cursor = conn.cursor()

    # Question 1: Total amount spent in each category
    st.subheader("1. Total Amount Spent in Each Category")
    cursor.execute("SELECT Category, SUM(Amount) AS Total_Spent FROM Expenses GROUP BY Category;")
    result1 = cursor.fetchall()
    df1 = pd.DataFrame(result1, columns=["Category", "Total Spent"])
    fig1 = px.bar(df1, x="Category", y="Total Spent", title="Total Amount Spent in Each Category", color="Total Spent")
    st.plotly_chart(fig1)

    # Question 2: Total amount spent using each payment mode
    st.subheader("2. Total Amount Spent Using Each Payment Mode")
    cursor.execute("SELECT Payment_Mode, SUM(Amount) AS Total_Spent FROM Expenses GROUP BY Payment_Mode;")
    result2 = cursor.fetchall()
    df2 = pd.DataFrame(result2, columns=["Payment Mode", "Total Spent"])
    fig2 = px.pie(df2, values="Total Spent", names="Payment Mode", title="Total Amount Spent Using Each Payment Mode")
    st.plotly_chart(fig2)

    # Question 3: Total cashback received across all transactions
    st.subheader("3. Total Cashback Received Across All Transactions")
    cursor.execute("SELECT SUM(Cashback) AS Total_Cashback FROM Expenses;")
    result3 = cursor.fetchone()
    st.metric(label="Total Cashback", value=f"₹{result3[0]:,.2f}")

    # Question 4: Top 5 most expensive categories
    st.subheader("4. Top 5 Most Expensive Categories")
    cursor.execute("SELECT Category, SUM(Amount) AS Total_Spent FROM Expenses GROUP BY Category ORDER BY Total_Spent DESC LIMIT 5;")
    result4 = cursor.fetchall()
    df4 = pd.DataFrame(result4, columns=["Category", "Total Spent"])
    fig4 = px.bar(df4, x="Category", y="Total Spent", title="Top 5 Most Expensive Categories", color="Total Spent")
    st.plotly_chart(fig4)

    # Question 5: Spending on transportation by payment mode
    st.subheader("5. Spending on Transportation by Payment Mode")
    cursor.execute("SELECT Payment_Mode, SUM(Amount) AS Total_Spent FROM Expenses WHERE Category = 'Travel' GROUP BY Payment_Mode;")
    result5 = cursor.fetchall()
    df5 = pd.DataFrame(result5, columns=["Payment Mode", "Total Spent"])
    fig5 = alt.Chart(df5).mark_bar().encode(
        x="Payment Mode:O",
        y="Total Spent:Q",
        color="Payment Mode:O",
        tooltip=["Payment Mode", "Total Spent"]
    ).properties(title="Spending on Transportation by Payment Mode")
    st.altair_chart(fig5, use_container_width=True)

    # Transactions with Cashback
    st.subheader("6. Transactions with Cashback")
    cursor.execute("SELECT Date, Category, Payment_Mode, Description, Amount, Cashback FROM Expenses WHERE Cashback > 0;")
    result = cursor.fetchall()
    df6 = pd.DataFrame(result, columns=["Date", "Category", "Payment Mode", "Description", "Amount", "Cashback"])
    fig6 = px.scatter(df6, x="Amount",y="Cashback",color="Category",title="Transactions with Cashback",hover_data=["Date", "Payment Mode", "Description"])
    st.plotly_chart(fig6)

    # Total Spending in Each Month
    st.subheader("7. Total Spending in Each Month")
    cursor.execute("SELECT MONTH(Date) AS Month, SUM(Amount) AS Total_Spent FROM Expenses GROUP BY MONTH(Date);")
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns=["Month", "Total Spent"])
    fig = alt.Chart(df).mark_bar().encode(
        x=alt.X("Month:O", title="Month"),
        y=alt.Y("Total Spent:Q", title="Total Spent"),
        tooltip=["Month", "Total Spent"]
    ).properties(title="Total Spending in Each Month")
    st.altair_chart(fig, use_container_width=True)

    # Spending in "Travel," "Entertainment," or "Gifts"
    st.subheader("8. Spending by Category (Travel, Entertainment, Gifts)")
    cursor.execute("SELECT MONTH(Date) AS Month, Category, SUM(Amount) AS Total_Spent FROM Expenses WHERE Category IN ('Travel', 'Entertainment', 'Gifts') GROUP BY MONTH(Date), Category ORDER BY Total_Spent DESC;")
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns=["Month", "Category", "Total Spent"])
    fig = px.bar(df,x="Month",y="Total Spent",color="Category",title="Spending in 'Travel,' 'Entertainment,' and 'Gifts' by Month")
    st.plotly_chart(fig)

    # Recurring Expenses by Month (Altair)
    st.subheader("9. Recurring Expenses by Month")
    cursor.execute("SELECT MONTH(Date) AS Month, Category, SUM(Amount) AS Total_Spent FROM Expenses GROUP BY MONTH(Date), Category ORDER BY Total_Spent DESC;")
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns=["Month", "Category", "Total Spent"])
    df["Month"] = df["Month"].apply(lambda x: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][x - 1])
    fig_altair = alt.Chart(df).mark_rect().encode(
        x=alt.X("Month:N", title="Month"),
        y=alt.Y("Category:N", title="Category", sort="-x"),
        color=alt.Color("Total Spent:Q", scale=alt.Scale(scheme="yellowgreenblue"), title="Total Spent"),
        tooltip=["Month", "Category", "Total Spent"]
    ).properties(title="Recurring Expenses by Month", width=700, height=400)
    st.altair_chart(fig_altair, use_container_width=True)

    # Cashback Earned Per Month
    st.subheader("10. Cashback Earned Per Month")
    cursor.execute("SELECT MONTH(Date) AS Month, SUM(Cashback) AS Total_Cashback FROM Expenses GROUP BY MONTH(Date);")
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns=["Month", "Total Cashback"])
    fig = alt.Chart(df).mark_line().encode(
        x=alt.X("Month:O", title="Month"),
        y=alt.Y("Total Cashback:Q", title="Total Cashback"),
        tooltip=["Month", "Total Cashback"]
    ).properties(title="Monthly Cashback Earned")
    st.altair_chart(fig, use_container_width=True)

    #How has your overall spending changed over time?
    st.subheader("11. Spending Over Time")
    cursor.execute("SELECT Date, SUM(Amount) AS Total_Spent FROM Expenses GROUP BY Date ORDER BY Date;")
    result6 = cursor.fetchall()
    df6 = pd.DataFrame(result6, columns=["Date", "Total Spent"])
    fig6 = px.line(df6, x="Date", y="Total Spent", title="Overall Spending Over Time")
    st.plotly_chart(fig6)

    #Typical costs associated with travel (e.g., flights, accommodation, transportation)
    st.subheader("12. Typical Costs Associated with Travel")
    cursor.execute("SELECT Description, SUM(Amount) AS Total_Spent FROM Expenses WHERE Category = 'Travel' GROUP BY Description ORDER BY Total_Spent DESC;")
    result7 = cursor.fetchall()
    df7 = pd.DataFrame(result7, columns=["Description", "Total Spent"])
    fig7 = px.bar(df7, x="Description", y="Total Spent", title="Costs Associated with Travel", color="Total Spent")
    st.plotly_chart(fig7)

    #Patterns in grocery spending (e.g., weekends, seasons)
    st.subheader("13. Patterns in Grocery Spending")
    cursor.execute("SELECT WEEKDAY(Date) AS Day, SUM(Amount) AS Total_Spent FROM Expenses WHERE Category = 'Groceries' GROUP BY Day ORDER BY Day;")
    result8 = cursor.fetchall()
    df8 = pd.DataFrame(result8, columns=["Day", "Total Spent"])
    df8["Day"] = df8["Day"].map({0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"})
    fig8 = px.bar(df8, x="Day", y="Total Spent", title="Grocery Spending by Day of the Week", color="Total Spent")
    st.plotly_chart(fig8)

    #High and low priority categories
    st.subheader("14. High and Low Priority Categories")
    cursor.execute("SELECT Category, SUM(Amount) AS Total_Spent FROM Expenses GROUP BY Category ORDER BY Total_Spent DESC;")
    result9 = cursor.fetchall()
    df9 = pd.DataFrame(result9, columns=["Category", "Total Spent"])
    fig9 = px.bar(df9, x="Category", y="Total Spent", title="Spending by Category (High vs. Low Priority)", color="Total Spent")
    st.plotly_chart(fig9)

    #Category contributing the highest percentage of total spending
    st.subheader("15. Category with the Highest Percentage of Total Spending")
    cursor.execute("SELECT Category, (SUM(Amount) / (SELECT SUM(Amount) FROM Expenses) * 100) AS Percentage FROM Expenses GROUP BY Category ORDER BY Percentage DESC;")
    result10 = cursor.fetchall()
    df10 = pd.DataFrame(result10, columns=["Category", "Percentage"])
    fig10 = px.pie(df10, values="Percentage", names="Category", title="Category Contribution to Total Spending")
    st.plotly_chart(fig10)




    