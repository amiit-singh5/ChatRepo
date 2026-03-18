# modification in poc2.py : openrouter key has been collected from the 3nv so now secure and can be pused to# git that ealier not allowing to push due to secrete key 
import streamlit as st
from openai import OpenAI
import os

api_key1=os.getenv("OPENROUTER_API_KEY")
print(api_key1)

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

st.title("AMIITSINGH AI Chat Room")

# conversation memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# chat input (always bottom)
user_input = st.chat_input("Ask a question")

if user_input:

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    response = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct",
        messages=st.session_state.messages
    )

    ai_reply = response.choices[0].message.content

    st.session_state.messages.append(
        {"role": "assistant", "content": ai_reply}
    )

    with st.chat_message("assistant"):
        st.write(ai_reply)

    # force auto scroll to bottom
    st.markdown(
        """
        <script>
        var body = window.parent.document.querySelector(".main");
        body.scrollTop = body.scrollHeight;
        </script>
        """,
        unsafe_allow_html=True
    )
