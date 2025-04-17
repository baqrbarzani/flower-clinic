import streamlit as st
from database import get_db_connection

def show_register():
    st.title("Doctor Registration")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if username and password:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                st.error("Username already exists.")
            else:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                conn.close()
                st.success("Registration successful! Please log in.")
        else:
            st.warning("Please enter both username and password.")
