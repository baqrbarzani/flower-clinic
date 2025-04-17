import streamlit as st
import sqlite3
import hashlib

# Create table for doctors
def init_db():
    conn = sqlite3.connect("clinic_visitors.db", check_same_thread=False)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Hash passwords for safety
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def show_sidebar():
    init_db()
    st.sidebar.title("👩‍⚕️ Clinic Login")

    # Tabs for login/register
    tab = st.sidebar.radio("Select", ["Login", "Register New Doctor"])

    if tab == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("🔐 Login"):
            conn = sqlite3.connect("clinic_visitors.db", check_same_thread=False)
            c = conn.cursor()
            c.execute("SELECT * FROM doctors WHERE username = ? AND password = ?", (username, hash_password(password)))
            doctor = c.fetchone()
            if doctor:
                st.session_state.logged_in = True
                st.session_state.doctor = username
                st.success("Logged in successfully.")
                st.experimental_rerun()
            else:
                st.error("Invalid credentials.")

    elif tab == "Register New Doctor":
        new_username = st.sidebar.text_input("New Username")
        new_password = st.sidebar.text_input("New Password", type="password")
        if st.sidebar.button("📝 Register"):
            if new_username and new_password:
                conn = sqlite3.connect("clinic_visitors.db", check_same_thread=False)
                c = conn.cursor()
                try:
                    c.execute("INSERT INTO doctors (username, password) VALUES (?, ?)", 
                              (new_username, hash_password(new_password)))
                    conn.commit()
                    st.success("Doctor registered successfully. You can now log in.")
                except sqlite3.IntegrityError:
                    st.warning("Username already exists.")
            else:
                st.warning("Please enter both username and password.")
