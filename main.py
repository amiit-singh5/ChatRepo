import streamlit as st
from auth.login import login
from services.chat_service import (
    start_new_chat,
    add_user_message,
    add_ai_message,
    fetch_messages,
    fetch_user_chats,
    fetch_archived_chats
)
from services.llm_service import get_ai_response
from services.db_service import get_user_id


st.title("AMIITSINGH AI Chat Room")

# ---------------- LOGIN ----------------
if not login():
    st.stop()



username = st.session_state.user
user_id = get_user_id(username)
#user_id = st.session_state.user_id

# ---------------- SESSION INIT ----------------
if "process_file" not in st.session_state:
    st.session_state.process_file = False

if "file_content" not in st.session_state:
    st.session_state.file_content = None

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

if "show_menu" not in st.session_state:
    st.session_state.show_menu = False

if "last_processed" not in st.session_state:
    st.session_state.last_processed = None

# ---------------- SIDEBAR ----------------
st.sidebar.subheader("Chats")

# ➕ New Chat
if st.sidebar.button("➕ New Chat"):
    chat_id = start_new_chat(user_id)
    st.session_state.current_chat = chat_id
    st.session_state.show_menu = False
    st.rerun()

# Active chats
user_chats = fetch_user_chats(user_id)

for chat in user_chats:
    col1, col2 = st.sidebar.columns([0.8, 0.2])

    with col1:
        if st.button(chat["title"], key=f"chat_{chat['id']}"):
            st.session_state.current_chat = chat["id"]
            st.session_state.show_menu = False

    with col2:
        with st.popover("⋮"):

            if st.button("🔗 Share", key=f"share_{chat['id']}"):
                st.code(f"http://localhost:8501/?chat_id={chat['id']}")

            new_name = st.text_input(
                "Rename",
                value=chat["title"],
                key=f"rename_input_{chat['id']}"
            )
            if st.button("✅ Save", key=f"rename_{chat['id']}"):
                from services.chat_service import update_chat_title
                update_chat_title(chat["id"], new_name)
                st.rerun()

            if st.button("🗑 Delete", key=f"delete_{chat['id']}"):
                from services.db_service import delete_chat
                delete_chat(chat["id"])
                if st.session_state.current_chat == chat["id"]:
                    st.session_state.current_chat = None
                st.rerun()

            if st.button("📦 Archive", key=f"archive_{chat['id']}"):
                from services.db_service import archive_chat
                archive_chat(chat["id"])
                st.rerun()

# -------- Archived Section --------
st.sidebar.divider()
st.sidebar.subheader("📦 Archived Chats")

archived_chats = fetch_archived_chats(user_id)

for chat in archived_chats:
    col1, col2 = st.sidebar.columns([0.7, 0.3])

    with col1:
        st.markdown(f"📦 {chat['title']}")

    with col2:
        if st.button("♻️", key=f"restore_{chat['id']}"):
            from services.db_service import restore_chat
            restore_chat(chat["id"])
            st.rerun()

# ---------------- ENSURE CHAT ----------------
if st.session_state.current_chat is None:
    st.session_state.current_chat = start_new_chat(user_id)

# ---------------- LOAD MESSAGES ----------------
messages = fetch_messages(st.session_state.current_chat)

for msg in messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------------- INPUT ----------------
col1, col2 = st.columns([0.92, 0.08])

with col1:
    user_input = st.chat_input("Ask a question", key="chat_input_main")

with col2:
    if st.button("➕"):
        st.session_state.show_menu = not st.session_state.show_menu

# ---------------- FILE UPLOAD ----------------
if st.session_state.show_menu:
    st.markdown("---")
    st.markdown("### 📎 Upload File")

    uploaded_file = st.file_uploader(
        "Upload a text file",
        type=["txt"],
        key=f"uploaded_file_{st.session_state.current_chat}"
    )

    if uploaded_file:
        file_content = uploaded_file.read().decode("utf-8")

        if st.button("📤 Send File"):
            st.session_state.file_content = file_content
            st.session_state.process_file = True
            st.rerun()

    if st.button("❌ Close Upload"):
        st.session_state.show_menu = False

# ---------------- FINAL INPUT ----------------
final_input = None

if st.session_state.process_file:
    final_input = st.session_state.file_content
elif user_input:
    final_input = user_input

# ---------------- PROCESS ----------------
if final_input is not None and st.session_state.current_chat is not None:

    # 🔥 FILE FLOW (always process)
    if st.session_state.process_file:

        st.session_state.process_file = False
        st.session_state.file_content = None

        add_user_message(st.session_state.current_chat, final_input)

        messages = fetch_messages(st.session_state.current_chat)

        if len(messages) == 1:
            from services.chat_service import update_chat_title
            update_chat_title(st.session_state.current_chat, final_input[:30])

        ai_reply = get_ai_response(messages)

        add_ai_message(st.session_state.current_chat, ai_reply)

        st.session_state.show_menu = False
        st.rerun()

    # 🔥 TEXT FLOW (avoid duplicates)
    elif final_input != st.session_state.last_processed:

        st.session_state.last_processed = final_input

        add_user_message(st.session_state.current_chat, final_input)

        messages = fetch_messages(st.session_state.current_chat)

        if len(messages) == 1:
            from services.chat_service import update_chat_title
            update_chat_title(st.session_state.current_chat, final_input[:30])

        ai_reply = get_ai_response(messages)

        add_ai_message(st.session_state.current_chat, ai_reply)

        st.session_state.show_menu = False
        st.rerun()