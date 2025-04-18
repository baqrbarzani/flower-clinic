import streamlit as st
from database import verify_user, add_user

def show_login():
    st.title("Clinic Visitor Login")
    menu = ["Login", "Register"]
    choice = st.selectbox("Menu", menu)

    if choice == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login")

        if login_button:
            if verify_user(username, password):
                st.session_state['authenticated'] = True
                st.success("Login successful!")
            else:
                st.error("Invalid username or password.")

    elif choice == "Register":
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        register_button = st.button("Register")

        if register_button:
            if add_user(new_username, new_password):
                st.success("Registration successful! You can now log in.")
            else:
                st.error("Username already exists. Please choose a different one.")
