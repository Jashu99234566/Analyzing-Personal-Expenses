# 💰 Expense Analysis Dashboard

## 📟 Overview

The **Expense Analysis Dashboard** is a Streamlit-powered interactive application that connects to a MySQL database to analyze personal spending habits. It enables users to run SQL-based queries, visualize their expense data, and uncover financial insights—all through a user-friendly web interface.

---

## 🧩 Key Features

* 🔍 **Interactive Visualizations**: View dynamic charts and summaries of your expense patterns.
* 📊 **Query Dropdown Menu**: Choose from 20 SQL-driven analytical questions to explore different aspects of your spending.
* 🧠 **Insights Delivered Visually**: Metrics, bar plots, pie charts, and line graphs powered by Plotly, Altair, and Matplotlib.
* 🏠 **Welcome Page**: Clear explanation of the project purpose and navigation guide.

---

## ⚙️ Technologies Used

| Category          | Tools & Libraries          |
| ----------------- | -------------------------- |
| **Frontend**      | Streamlit                  |
| **Backend**       | MySQL (via PyMySQL)        |
| **Visualization** | Plotly, Altair, Matplotlib |
| **Data Handling** | Pandas                     |

---

## 📂 Folder Structure

```
├── exp.py                  # Main Streamlit App with 20 queries
├── expense.ipynb           # Jupyter Notebook version (optional)
└── data/ExpenseDB          # MySQL Database (local or remote setup required)
```

---

## ✅ How It Works

1. User launches the app via Streamlit.
2. Connects to MySQL database containing expense data.
3. Selects a query from the dropdown list.
4. App displays charts or metrics answering that specific question.

---

## 🔐 Prerequisites

* Python ≥ 3.7
* MySQL Server running locally with `ExpenseDB` and `Expenses` table
* Install Python dependencies:

```bash
pip install streamlit pymysql pandas matplotlib altair plotly
```

---

## 🚀 Run the App

```bash
streamlit run exp.py
```

Make sure the MySQL server is running before launching the app.

---

## 📌 Sample Questions Answered

* What category do I spend the most on?
* How does my cashback vary by month?
* Are weekends more expensive than weekdays?
* What are my top recurring expenses?

---

Feel free to contribute or fork this project for your own expense dashboard customization.
