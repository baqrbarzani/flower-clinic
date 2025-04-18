import streamlit as st
from database import verify_user

def show_login():
    st.title("Clinic Visitor Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if verify_user(username, password):
            st.session_state['authenticated'] = True
            st.success("Login successful!")
        else:
            st.error("Invalid username or password.")
