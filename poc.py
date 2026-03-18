# initial proof of concept : ai chat
# what ever you type , it display on screen, question goes to openrouter free Meta LLama
print("this is ai chat")
import streamlit as st
from openai import OpenAI

# create client
client = OpenAI(
    api_key=''
)

# send request
from openai import OpenAI
apikey="",
base_url="https://openrouter.ai/api/v1"
client = OpenAI(
    api_key="",
    base_url="https://openrouter.ai/api/v1",
    
)


st.title("AMIITSINGH AI Chat Room")

# initialize session memory
if "history" not in st.session_state:
    st.session_state.history = []

if "active" not in st.session_state:
    st.session_state.active = True

user_input = st.text_input("Ask a question")

if user_input and st.session_state.active:

    if user_input.lower() in ["quit", "exit", "bye"]:
        st.session_state.active = False
        st.write("Chat ended. Goodbye!")
    else:
        msg = user_input.lower() #"Explain nuclear fusion in simple terms"
        message_to_llama = [
        {"role": "user", "content": msg}
        ]
        response = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct",
        messages=message_to_llama
        )

        st.session_state.history.append(response.choices[0].message.content)

# display previous questions
for q in st.session_state.history:
    st.write("You:", q)
