 # Create a Streamlit web application that allows users to connect to a MySQL database and ask natural language questions. The app should generate and execute SELECT SQL queries using an LLM and display both the query results and a simple English explanation.

# Note:
# Use the sample MySQL connection parameters provided in connection.txt and the sample database schema in db.txt for testing.

# pip install mysql-connector-python

import streamlit as st
import mysql.connector
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
 
load_dotenv()

st.set_page_config(page_title="NL to SQL (MySQL)", layout="centered")
st.title("Natural Language to SQL (MySQL)")
 
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@Bhargavi45",
    database="cdac"
)

cursor = conn.cursor()
 
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)
 
cursor.execute("DESCRIBE employees")
schema = cursor.fetchall()

st.subheader("Table: employees")
st.write(schema)
 
question = st.text_input("Ask a question about employees:")

if question:
     
    sql_prompt = f"""
    You are an expert MySQL developer.

    Table name: employees
    Table schema: {schema}

    Convert the following English question into a valid MySQL SELECT query.
    Use ONLY SELECT statements.
    Do NOT use INSERT, UPDATE, DELETE.
    Output only SQL query and nothing else.

    Question: {question}
    """

    sql_query = llm.invoke(sql_prompt).content.strip()

    st.subheader("Generated SQL Query")
    st.code(sql_query, language="sql")

    try:
        cursor.execute(sql_query)
        result = cursor.fetchall()

        st.subheader("Query Result")
        st.dataframe(result)
 
        explain_prompt = f"""
        Explain the result of this SQL query in simple English.

        SQL Query:
        {sql_query}

        Result:
        {result}
        """

        explanation = llm.invoke(explain_prompt).content

        st.subheader("Explanation")
        st.write(explanation)

    except Exception as e:
        st.error(f"Error executing query: {e}")

conn.close()

