import requests
import streamlit as st
import time

def gemini_chat():
    st.subheader("LLM (Local Server)")

    api_key = "dummy-key"
    url = "http://192.168.52.59:1234/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
 
    if "gemini_messages" not in st.session_state:
        st.session_state.gemini_messages = []
 
    for msg in st.session_state.gemini_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_prompt = st.chat_input("Ask Anything...")

    if user_prompt:
        st.session_state.gemini_messages.append(
            {"role": "user", "content": user_prompt}
        )

        with st.chat_message("user"):
            st.write(user_prompt)

        req_data = {
            "model": "google/gemma-3-4b",
            "messages": st.session_state.gemini_messages,
        }

        time1 = time.perf_counter()
        response = requests.post(url, json=req_data, headers=headers)
        time2 = time.perf_counter()

        if response.status_code == 200:
            resp = response.json()
            reply = resp["choices"][0]["message"]["content"]
 
            st.session_state.gemini_messages.append(
                {"role": "assistant", "content": reply}
            )

            with st.chat_message("assistant"):
                st.write(reply)

            st.caption(f"Time required: {time2 - time1:.2f} sec")
        else:
            st.error(response.text)
