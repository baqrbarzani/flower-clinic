import streamlit as st
from database import get_db_connection
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def show_login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
        user = cursor.fetchone()
        conn.close()
        if user:
            st.success(f"Welcome, {username}!")
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
        else:
            st.error("Invalid username or password")
