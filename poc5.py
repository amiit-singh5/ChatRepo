import streamlit as st
from openai import OpenAI
import os
import uuid

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

st.title("AMIITSINGH AI Chat Room")

# -------- Get chat id --------
params = st.query_params
chat_id = params.get("chat_id")

if not chat_id:
    chat_id = str(uuid.uuid4())
    st.query_params["chat_id"] = chat_id

# -------- Chat storage --------
if "chats" not in st.session_state:
    st.session_state.chats = {}

if chat_id not in st.session_state.chats:
    st.session_state.chats[chat_id] = []

messages = st.session_state.chats[chat_id]

# -------- Sidebar --------
st.sidebar.title("Chats")

new_chat_id = str(uuid.uuid4())

st.sidebar.markdown(
    f'<a href="?chat_id={new_chat_id}" target="_blank">➕ New Chat</a>',
    unsafe_allow_html=True
)

# -------- Show messages --------
for msg in messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -------- Chat input --------
user_input = st.chat_input("Ask something")

if user_input:

    messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    response = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct",
        messages=messages
    )

    ai_reply = response.choices[0].message.content

    messages.append({"role": "assistant", "content": ai_reply})

    with st.chat_message("assistant"):
        st.write(ai_reply)
