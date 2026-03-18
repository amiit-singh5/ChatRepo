# chat that store with chat name as first question asked
import streamlit as st
from openai import OpenAI
import os
import uuid

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

st.title("AMIITSINGH AI Chat Room")

# -------- Init --------
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    new_id = str(uuid.uuid4())
    st.session_state.current_chat = new_id
    st.session_state.chats[new_id] = {
        "title": "New Chat",
        "messages": []
    }

# -------- Sidebar --------
st.sidebar.title("Chats")

# New chat
if st.sidebar.button("➕ New Chat"):
    new_id = str(uuid.uuid4())
    st.session_state.chats[new_id] = {
        "title": "New Chat",
        "messages": []
    }
    st.session_state.current_chat = new_id

# Show chats with TITLE
for chat_id, chat_data in st.session_state.chats.items():
    title = chat_data["title"]
    if st.sidebar.button(title):
        st.session_state.current_chat = chat_id

# -------- Current chat --------
chat_data = st.session_state.chats[st.session_state.current_chat]
messages = chat_data["messages"]

# -------- Display messages --------
for msg in messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -------- Input --------
user_input = st.chat_input("Ask something")

if user_input:

    # Save user message
    messages.append({"role": "user", "content": user_input})

    # 🟢 SET TITLE IF FIRST MESSAGE
    if chat_data["title"] == "New Chat":
        chat_data["title"] = user_input[:30]  # limit length

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
