#  Q1:
# Create a Streamlit application that allows users to upload a CSV file and view its schema.
# Use an LLM to convert user questions into SQL queries, execute them on the CSV data using pandasql,
# and explain the results in simple English.

import streamlit as st
import pandas as pd
import pandasql as ps
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
 
load_dotenv()

st.set_page_config(page_title="CSV SQL Query App")
st.title("CSV Query using LLM")
 
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)
 
data_file = st.file_uploader("Upload a CSV file", type=["csv"])

if data_file:
    df = pd.read_csv(data_file)

    st.subheader("CSV Data")
    st.dataframe(df)

    st.subheader("CSV Schema")
    st.write(df.dtypes)

    user_question = st.chat_input("Ask a question about this CSV")

    if user_question:
        
        sql_prompt = f"""
You are an expert SQLite developer with 10 years of experience.

Table name: data

Table schema:
{df.dtypes}

User question:
{user_question}

Instruction:
- Write ONLY the SQL query
- Do not explain
- Use table name as data
- If impossible, reply with: I don't know
"""

        sql_query = llm.invoke(sql_prompt).content.strip()

        st.subheader("Generated SQL Query")
        st.code(sql_query, language="sql")

        if sql_query.lower() != "i don't know":
            try: 
                result = ps.sqldf(sql_query, {"data": df})

                st.subheader("Query Result")
                st.dataframe(result)
 
                explain_prompt = f"""
Explain the following result in very simple English.

User question:
{user_question}

SQL Query:
{sql_query}

Result:
{result.head()}
"""

                explanation = llm.invoke(explain_prompt).content

                st.subheader("Explanation")
                st.success(explanation)

            except Exception as e:
                st.error(f"SQL Execution Error: {e}")
        else:
            st.warning("LLM could not generate SQL for this question.")
