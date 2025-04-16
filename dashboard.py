import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

def show_dashboard():
    if not st.session_state.get("logged_in"):
        return

    doctor = st.session_state.doctor
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
                ''', (doctor, name, reason, timestamp))
                conn.commit()
                st.success("Visitor added successfully.")
            else:
                st.warning("Please fill in all fields.")

    st.divider()
    st.subheader(f"📋 Visitor List for {doctor}")

    df = pd.read_sql_query(f'''
        SELECT name, reason, timestamp FROM visitors
        WHERE doctor = ?
        ORDER BY timestamp DESC
    ''', conn, params=(doctor,))

    if not df.empty:
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download as CSV",
            data=csv,
            file_name=f"{doctor}_visitors.csv",
            mime='text/csv'
        )
    else:
        st.info("No visitors recorded yet.")
