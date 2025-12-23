

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
