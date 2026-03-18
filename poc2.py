# modiled poc.py : user ask queston and get anser from llama and print on chat scenn and scroll up for next question
import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key="",
    base_url="https://openrouter.ai/api/v1"
)

st.title("AMIITSINGH AI Chat Room")

# store conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# chat input (auto clears after submit)
user_input = st.chat_input("Ask a question")

if user_input:

    # show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    # call model
    response = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct",
        messages=st.session_state.messages
    )

    ai_reply = response.choices[0].message.content

    # store AI response
    st.session_state.messages.append(
        {"role": "assistant", "content": ai_reply}
    )

    with st.chat_message("assistant"):
        st.write(ai_reply)
