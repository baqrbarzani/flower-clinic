import streamlit as st
from database import get_db_connection

def show_login():
    st.title("Doctor Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            conn.close()

            if result and result[0] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome, Dr. {username}!")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password.")
        else:
            st.warning("Please enter both username and password.")
