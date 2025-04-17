import streamlit as st
import sqlite3
import hashlib

# Initialize doctor table
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

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def show_sidebar():
    init_db()
    st.sidebar.title("👨‍⚕️ Clinic Portal")

    # Create tab for choosing between Login and Register
    tab = st.sidebar.radio("Select Action", ["Login", "Register New Doctor"], index=0)

    # Registration Form
    if tab == "Register New Doctor":
        st.sidebar.subheader("Register a New Doctor")
        new_user = st.sidebar.text_input("New Username")
        new_pass = st.sidebar.text_input("New Password", type="password")
        confirm_pass = st.sidebar.text_input("Confirm Password", type="password")

        if st.sidebar.button("📝 Register"):
            if new_user and new_pass and confirm_pass:
                if new_pass == confirm_pass:
                    try:
                        # Insert the new doctor into the database
                        conn = sqlite3.connect("clinic_visitors.db", check_same_thread=False)
                        c = conn.cursor()
                        c.execute("INSERT INTO doctors (username, password) VALUES (?, ?)", 
                                  (new_user, hash_password(new_pass)))
                        conn.commit()

                        # Log the user in automatically after successful registration
                        st.session_state.logged_in = True
                        st.session_state.doctor = new_user
                        st.success(f"Doctor {new_user} registered and logged in successfully.")
                        st.rerun()  # Refresh the page to reflect logged-in state

                    except sqlite3.IntegrityError:
                        st.warning("Username already exists.")
                else:
                    st.warning("Passwords do not match.")
            else:
                st.warning("Please provide both username and password.")

    # Login Form
    elif tab == "Login":
        st.sidebar.subheader("Login")
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
                st.success("Login successful.")
                st.rerun()  # Refresh the page to reflect logged-in state
            else:
                st.error("Incorrect username or password.")
