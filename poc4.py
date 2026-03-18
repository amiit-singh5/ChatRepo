import streamlit as st
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

st.title("AMIITSINGH AI Chat Room")

# initialize chats
if "chats" not in st.session_state:
    st.session_state.chats = {"Chat 1": []}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"


# ---- Sidebar ----
st.sidebar.title("Chats")

# new chat button
if st.sidebar.button("➕ New Chat"):
    new_chat_name = f"Chat {len(st.session_state.chats) + 1}"
    st.session_state.chats[new_chat_name] = []
    st.session_state.current_chat = new_chat_name

# list chats
for chat_name in st.session_state.chats:
    if st.sidebar.button(chat_name):
        st.session_state.current_chat = chat_name


# ---- Display current chat ----
messages = st.session_state.chats[st.session_state.current_chat]

for msg in messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# ---- Chat input ----
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
