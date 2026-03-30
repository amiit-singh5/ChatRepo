import streamlit as st
from auth.login import login
from services.chat_service import (
    start_new_chat,
    add_user_message,
    add_ai_message,
    fetch_messages,
    fetch_user_chats
)
from services.llm_service import get_ai_response

st.title("AMIITSINGH AI Chat Room")

# ---------------- LOGIN ----------------
if not login():
    st.stop()

user_id = 1  # keep stable for now

# ---------------- SESSION INIT ----------------
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

if "file_processed" not in st.session_state:
    st.session_state.file_processed = False

if "show_menu" not in st.session_state:
    st.session_state.show_menu = False

# ---------------- SIDEBAR ----------------
st.sidebar.subheader("Chats")

if st.sidebar.button("➕ New Chat"):
    chat_id = start_new_chat(user_id)
    st.session_state.current_chat = chat_id

    st.session_state.file_processed = False
    st.session_state.show_menu = False

    st.rerun()  # 🔥 important

# load chats
user_chats = fetch_user_chats(user_id)

for chat in user_chats:
    col1, col2 = st.sidebar.columns([0.8, 0.2])

    # Chat title (click to load)
    with col1:
        if st.button(chat["title"], key=f"chat_{chat['id']}"):
            st.session_state.current_chat = chat["id"]
            st.session_state.file_processed = False
            st.session_state.show_menu = False

    # 3-dot menu
    with col2:
        with st.popover("⋮", use_container_width=True):

            # 🔗 Share
            if st.button("🔗 Share", key=f"share_{chat['id']}"):
                share_link = f"http://localhost:8501/?chat_id={chat['id']}"
                st.write("Copy link:")
                st.code(share_link)

            # ✏️ Rename
            new_name = st.text_input(
                "Rename",
                value=chat["title"],
                key=f"rename_input_{chat['id']}"
            )
            if st.button("✅ Save", key=f"rename_{chat['id']}"):
                from services.chat_service import update_chat_title
                update_chat_title(chat["id"], new_name)
                st.rerun()

            # 🗑 Delete
            if st.button("🗑 Delete", key=f"delete_{chat['id']}"):
                from services.db_service import delete_chat
                delete_chat(chat["id"])

                # if current chat deleted → reset
                if st.session_state.current_chat == chat["id"]:
                    st.session_state.current_chat = None

                st.rerun()

            # 📦 Archive
            if st.button("📦 Archive", key=f"archive_{chat['id']}"):
                from services.db_service import archive_chat
                archive_chat(chat["id"])
                st.rerun()
        st.session_state.file_processed = False
        st.session_state.show_menu = False

# ensure chat exists
if st.session_state.current_chat is None:
    st.session_state.current_chat = start_new_chat(user_id)
# if not st.session_state.current_chat and user_chats:
#     st.session_state.current_chat = user_chats[0]["id"]

# ---------------- LOAD MESSAGES ----------------
messages = []
if st.session_state.current_chat:
    messages = fetch_messages(st.session_state.current_chat)

# display messages
for msg in messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------------- INPUT + BUTTON ----------------
col1, col2 = st.columns([0.92, 0.08])

with col1:
    user_input = st.chat_input("Ask a question", key="chat_input_main")

with col2:
    if st.button("➕"):
        st.session_state.show_menu = not st.session_state.show_menu

# ---------------- FILE UPLOAD ----------------
file_content = None

if st.session_state.get("show_menu", False):
    st.markdown("---")
    st.markdown("### 📎 Upload File")

    uploaded_file = st.file_uploader(
        "Upload a text file",
        type=["txt"],
        key=f"uploaded_file_{st.session_state.current_chat}"
    )

    if uploaded_file and not st.session_state.file_processed:
        file_content = uploaded_file.read().decode("utf-8")

    if st.button("❌ Close Upload"):
        st.session_state.show_menu = False

# ---------------- FINAL INPUT ----------------
final_input = user_input if user_input else None

if file_content:
    final_input = file_content


if "last_processed" not in st.session_state:
    st.session_state.last_processed = None
# ---------------- PROCESS ----------------
if (final_input is not None and st.session_state.current_chat is not None  and final_input != st.session_state.last_processed ):
    st.session_state.last_processed = final_input
    if file_content:
        st.session_state.file_processed = True

    # save user message
    add_user_message(st.session_state.current_chat, final_input)

    # fetch updated messages
    messages = fetch_messages(st.session_state.current_chat)

    # update title (first message only)
    if len(messages) == 1:
        from services.chat_service import update_chat_title
        update_chat_title(st.session_state.current_chat, final_input[:30])

    # get AI response
    ai_reply = get_ai_response(messages)

    # save AI response
    add_ai_message(st.session_state.current_chat, ai_reply)

    # reset UI
    st.session_state.show_menu = False
    #st.session_state["chat_input_main"] = ""

    st.rerun()