import streamlit as st
import time
 
if "messages" not in st.session_state:
    st.session_state.messages = []
 
with st.sidebar:
    st.header("Settings")
    choices = ["Upper", "Lower", "Toggle"]
    mode = st.selectbox("Select Mode", choices)
    count = st.slider("Message Count", 1, 10, 6, 2)

st.title("Chatbot")
 
def stream_text(text, delay=0.05):
    for ch in text:
        yield ch
        time.sleep(delay)
 
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

 
user_msg = st.chat_input("Ask a question")

if user_msg:
   
    st.session_state.messages.append({
        "role": "user",
        "content": user_msg
    })
    with st.chat_message("user"):
        st.write(user_msg)
 
    if mode == "Upper":
        bot_reply = user_msg.upper()
    elif mode == "Lower":
        bot_reply = user_msg.lower()
    else:
        bot_reply = user_msg.swapcase()
 
    with st.chat_message("assistant"):
        st.write_stream(stream_text(bot_reply))
 
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })
