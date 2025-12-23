# Create a Streamlit web application that allows users to connect to a MySQL database and ask natural language questions. The app should generate and execute SELECT SQL queries using an LLM and display both the query results and a simple English explanation.

# Note:
# Use the sample MySQL connection parameters provided in connection.txt and the sample database schema in db.txt for testing.

# pip install mysql-connector-python

import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@Bhargavi45",
    database="cdac"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM employees")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
