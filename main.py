
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
# login
if not login():
    st.stop()

# 🔹 TEMP: user_id mapping
user_id = 1   # later replace with DB user id

# session init
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

# sidebar
st.sidebar.subheader("Chats")

if st.sidebar.button("➕ New Chat"):
    chat_id = start_new_chat(user_id)
    st.session_state.current_chat = chat_id

# load chats
user_chats = fetch_user_chats(user_id)

for chat in user_chats:
    if st.sidebar.button(chat["title"], key=chat["id"]):
        st.session_state.current_chat = chat["id"]

# ensure chat exists
if not st.session_state.current_chat and user_chats:
    st.session_state.current_chat = user_chats[0]["id"]

# load messages
messages = []
if st.session_state.current_chat:
    messages = fetch_messages(st.session_state.current_chat)

# display messages
for msg in messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# input
user_input = st.chat_input("Ask a question")
#user_input = st.chat_input("Ask a question")

if user_input and st.session_state.current_chat:

    # 1. save user message
    add_user_message(st.session_state.current_chat, user_input)
    # update title only if first message
    messages = fetch_messages(st.session_state.current_chat)

if len(messages) == 1:  # first message only
    from services.chat_service import update_chat_title
    update_chat_title(st.session_state.current_chat, user_input[:30])

    # 2. fetch updated messages
    updated_messages = fetch_messages(st.session_state.current_chat)

    # 3. get AI response
    ai_reply = get_ai_response(updated_messages)

    # DEBUG (optional)
    st.write("DEBUG AI:", ai_reply)

    # 4. save AI response
    add_ai_message(st.session_state.current_chat, ai_reply)

    # 5. FORCE reload UI
    st.session_state.messages = fetch_messages(st.session_state.current_chat)

    st.rerun()

#ai_reply = get_ai_response(messages + [{"role": "user", "content": user_input}])

#st.write("DEBUG AI:", ai_reply)   # 👈 ADD THIS






# import streamlit as st
# from auth.login import login
# from utils.session import (
#     init_session, create_new_chat,
#     get_user_chats, get_current_messages, add_message
# )
# from services.llm_service import get_ai_response
# from services.db_service import save_message, load_messages

# st.title("AMIITSINGH AI Chat Room")

# # login
# if not login():
#     st.stop()

# username = st.session_state.user
# st.sidebar.write(f"Logged in as: {username}")

# init_session()

# # 🔹 Sidebar - Chat list
# st.sidebar.subheader("Chats")

# if st.sidebar.button("➕ New Chat"):
#     create_new_chat(username)

# user_chats = get_user_chats(username)

# for chat_id, chat_data in user_chats.items():
#     if st.sidebar.button(chat_data["title"]):
#         st.session_state.current_chat = chat_id

# messages = get_current_messages(username)

# # display messages
# for msg in messages:
#     with st.chat_message(msg["role"]):
#         st.write(msg["content"])

# # input
# user_input = st.chat_input("Ask a question")

# if user_input:
#     add_message(username, "user", user_input)

#     with st.chat_message("user"):
#         st.write(user_input)

#     ai_reply = get_ai_response(messages)

#     add_message(username, "assistant", ai_reply)

#     with st.chat_message("assistant"):
#         st.write(ai_reply)
