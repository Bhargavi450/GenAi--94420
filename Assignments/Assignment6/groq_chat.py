import os
import requests
import time
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def groq_chat():
    st.subheader("Groq Chatbot")

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("API key not found")
        st.stop()

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Initialize history
    if "groq_messages" not in st.session_state:
        st.session_state.groq_messages = []

    # Show history
    for msg in st.session_state.groq_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_prompt = st.chat_input("Ask something...")

    if user_prompt:
        st.session_state.groq_messages.append(
            {"role": "user", "content": user_prompt}
        )

        with st.chat_message("user"):
            st.write(user_prompt)

        req_data = {
            "model": "llama-3.3-70b-versatile",
            "messages": st.session_state.groq_messages,
        }

        time1 = time.perf_counter()
        response = requests.post(url, json=req_data, headers=headers)
        time2 = time.perf_counter()

        if response.status_code == 200:
            resp = response.json()
            reply = resp["choices"][0]["message"]["content"]

            st.session_state.groq_messages.append(
                {"role": "assistant", "content": reply}
            )

            with st.chat_message("assistant"):
                st.write(reply)

            st.caption(f"Time required: {time2 - time1:.2f} sec")
        else:
            st.error(response.text)
