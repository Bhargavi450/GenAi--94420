from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
import streamlit as st

st.title("CHATBOT")
load_dotenv()

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)
 
if "conversation" not in st.session_state:
    st.session_state.conversation = [
        {"role": "system", "content": "You are a helpful assistant"}
    ]
 
user_input = st.chat_input("Ask Anythingg:")

if user_input:
    user_msg = {"role": "user", "content": user_input}
    st.session_state.conversation.append(user_msg)

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        def stream_response():
            full_response = ""
            for chunk in llm.stream(user_input):
                if chunk.content:
                    full_response += chunk.content
                    yield chunk.content
            
            st.session_state.conversation.append(
                {"role": "assistant", "content": full_response}
            )

        st.write_stream(stream_response())
