import streamlit as st
import pandas as pd

st.markdown("#CSV File Uploader")

data_file=st.file_uploader("Upload a CSV File",type=["csv"])
if data_file:
    df=pd.read_csv(data_file)
    st.dataframe(df)
    
