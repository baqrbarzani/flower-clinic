import streamlit as st
from database import get_db_connection
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def show_register():
    st.subheader("Register")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    if st.button("Register"):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
            conn.commit()
            st.success("Registration successful. You can now log in.")
        except sqlite3.IntegrityError:
            st.error("Username already exists. Please choose a different one.")
        conn.close()
