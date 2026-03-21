import streamlit as st
from auth.login import login
from utils.session import (
    init_session, create_new_chat,
    get_user_chats, get_current_messages, add_message
)
from services.llm_service import get_ai_response

st.title("AMIITSINGH AI Chat Room")

# login
if not login():
    st.stop()

username = st.session_state.user
st.sidebar.write(f"Logged in as: {username}")

init_session()

# 🔹 Sidebar - Chat list
st.sidebar.subheader("Chats")

if st.sidebar.button("➕ New Chat"):
    create_new_chat(username)

user_chats = get_user_chats(username)

for chat_id, chat_data in user_chats.items():
    if st.sidebar.button(chat_data["title"]):
        st.session_state.current_chat = chat_id

messages = get_current_messages(username)

# display messages
for msg in messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# input
user_input = st.chat_input("Ask a question")

if user_input:
    add_message(username, "user", user_input)

    with st.chat_message("user"):
        st.write(user_input)

    ai_reply = get_ai_response(messages)

    add_message(username, "assistant", ai_reply)

    with st.chat_message("assistant"):
        st.write(ai_reply)
