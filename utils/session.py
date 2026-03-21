import streamlit as st
import uuid

def init_session():
    if "all_chats" not in st.session_state:
        st.session_state.all_chats = {}

    if "current_chat" not in st.session_state:
        st.session_state.current_chat = None


def create_new_chat(username):
    import uuid
    chat_id = str(uuid.uuid4())[:8]

    if username not in st.session_state.all_chats:
        st.session_state.all_chats[username] = {}

    st.session_state.all_chats[username][chat_id] = {
        "title": "New Chat",
        "messages": []
    }

    st.session_state.current_chat = chat_id

def get_user_chats(username):
    return st.session_state.all_chats.get(username, {})

def get_current_messages(username):
    chats = get_user_chats(username)

    if not chats:
        create_new_chat(username)
        chats = get_user_chats(username)

    if (
        not st.session_state.current_chat
        or st.session_state.current_chat not in chats
    ):
        st.session_state.current_chat = list(chats.keys())[0]

    return chats[st.session_state.current_chat]["messages"]

def add_message(username, role, content):
    chat = st.session_state.all_chats[username][st.session_state.current_chat]

    # set title only for first user message
    if role == "user" and chat["title"] == "New Chat":
        chat["title"] = content[:30]  # first 30 chars

    chat["messages"].append({
        "role": role,
        "content": content
    })
