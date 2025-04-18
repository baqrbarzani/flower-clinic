import streamlit as st
from login import show_login
from register import show_register
from dashboard import show_dashboard

def main():
    st.title("Flower Clinic App")

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        show_dashboard()
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ""
    else:
        menu = ["Login", "Register"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Login":
            show_login()
        elif choice == "Register":
            show_register()

if __name__ == "__main__":
    main()
