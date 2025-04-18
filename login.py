import streamlit as st
from database import verify_user, add_user

def show_login():
    st.title("Login")

    menu = ["Login", "Sign Up"]
    choice = st.selectbox("Menu", menu)

    if choice == "Login":
        st.subheader("Login Section")

        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

        if st.button("Login"):
            if verify_user(username, password):
                st.success(f"Welcome {username}!")
                # Proceed to the main application
            else:
                st.error("Invalid Username or Password")

    elif choice == "Sign Up":
        st.subheader("Create New Account")

        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Sign Up"):
            if add_user(new_user, new_password):
                st.success("You have successfully created an account")
                st.info("Go to Login Menu to login")
            else:
                st.error("Username already exists")
