# login.py
import streamlit as st
import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def show_login():
    st.title("Doctor Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            conn = sqlite3.connect("clinic_visitors.db")
            c = conn.cursor()
            c.execute("SELECT password FROM doctors WHERE username = ?", (username,))
            result = c.fetchone()
            conn.close()

            if result and hash_password(password) == result[0]:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome, Dr. {username}!")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password.")
        else:
            st.warning("Please enter both username and password.")
