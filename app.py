import streamlit as st
from login import show_login
from register import show_register
from dashboard import show_dashboard

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Login", "Register", "Dashboard"])

    if page == "Login":
        show_login()
    elif page == "Register":
        show_register()
    elif page == "Dashboard":
        show_dashboard()

if __name__ == "__main__":
    main()
