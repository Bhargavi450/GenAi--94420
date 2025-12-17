#Q1: Design a Streamlit-based application with a sidebar to switch between Groq and LM Studio.
# The app should accept a user question and display responses using Groq’s cloud LLM and a locally running LM Studio model.
# Also maintain and display the complete chat history of user questions and model responses.
import streamlit as st
import gemini_chat
import groq_chat

st.title("Bhargavi's Chatbot")

with st.sidebar:
    st.header("AI Options")
    mode = st.selectbox("Select AI", ["GROQ", "LLM"])

if mode == "GROQ":
    groq_chat.groq_chat()

elif mode == "LLM":
    gemini_chat.gemini_chat()


