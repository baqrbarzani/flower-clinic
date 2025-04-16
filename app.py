import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Clinic Visitor Manager", layout="centered")

# SQLite setup
conn = sqlite3.connect("clinic_visitors.db", check_same_thread=False)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS visitors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor TEXT,
        name TEXT,
        reason TEXT,
        timestamp TEXT
    )
''')
conn.commit()

# Doctor passwords (For demo purposes; store securely in production)
doctor_credentials = {
    "Dr. Smith": "smith123",
    "Dr. Johnson": "johnson123",
    "Dr. Patel": "patel123",
    "Dr. Lee": "lee123"
}

st.title("🔐 Doctor Login")

# Login form
with st.form("login_form"):
    doctor_name = st.selectbox("Select your name", list(doctor_credentials.keys()))
    password = st.text_input("Enter password", type="password")
    login_btn = st.form_submit_button("Login")

if login_btn:
    if password == doctor_credentials.get(doctor_name):
        st.session_state.logged_in = True
        st.session_state.doctor = doctor_name
    else:
        st.error("Incorrect password.")

# After login
if st.session_state.get("logged_in"):
    st.success(f"Welcome, {st.session_state.doctor}!")

    st.subheader("📝 Register a new visitor")

    with st.form("visitor_form"):
        name = st.text_input("Visitor's name")
        reason = st.text_area("Reason for visit")
        submitted = st.form_submit_button("Add Visitor")

        if submitted:
            if name and reason:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute('''
                    INSERT INTO visitors (doctor, name, reason, timestamp)
                    VALUES (?, ?, ?, ?)
                ''', (st.session_state.doctor, name, reason, timestamp))
                conn.commit()
                st.success("Visitor added successfully.")
            else:
                st.warning("Please fill in all fields.")

    st.divider()
    st.subheader(f"📋 Visitor List for {st.session_state.doctor}")

    df = pd.read_sql_query(f'''
        SELECT name, reason, timestamp FROM visitors
        WHERE doctor = ?
        ORDER BY timestamp DESC
    ''', conn, params=(st.session_state.doctor,))

    if not df.empty:
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download as CSV",
            data=csv,
            file_name=f"{st.session_state.doctor}_visitors.csv",
            mime='text/csv'
        )
    else:
        st.info("No visitors recorded yet.")

