import streamlit as st
st.title("Hello , Streamlit!")
st.header("This is my first Streamlit program")
st.write("Welcome to Streamlit programming")
if st.button("click mee!",type="primary"):
    st.success("You clicked me!")