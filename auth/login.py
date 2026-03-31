import streamlit as st
from services.db_service import verify_user

def login():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user_id = verify_user(username, password)

        if user_id:
            st.session_state.authenticated = True
            st.session_state.user = username
            st.session_state.user_id = user_id
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

    return False