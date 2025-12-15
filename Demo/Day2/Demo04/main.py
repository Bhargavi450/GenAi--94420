import pandas as pd
import streamlit as st
import pandasql as ps

st.title("CSV Explorer")

data_file = st.file_uploader("Upload a CSV file", type=["csv"])

if data_file:
    df = pd.read_csv(data_file)
    st.dataframe(df)

    query = "SELECT * FROM df WHERE price > 50"
    result = ps.sqldf(query, {"df": df})

    st.write("Query Result:")
    st.dataframe(result)
