import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
import plotly.express as px

def show_dashboard():
    if not st.session_state.get("logged_in"):
        st.info("Please log in from the sidebar to continue.")
        return

    doctor = st.session_state.doctor

    # Connect to SQLite
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

    st.header("📝 Register a New Visitor")

    with st.form("visitor_form"):
        name = st.text_input("Visitor's Name")
        reason = st.text_area("Reason for Visit")
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

    # Load visitor data
    df = pd.read_sql_query('''
        SELECT name, reason, timestamp FROM visitors
        WHERE doctor = ?
    ''', conn, params=(doctor,))
    if df.empty:
        st.info("No visitors recorded yet.")
        return

    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Filters
    st.divider()
    st.subheader("🔍 Visitor Filters")

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", df['timestamp'].min().date())
    with col2:
        end_date = st.date_input("End Date", df['timestamp'].max().date())

    keyword = st.text_input("Search by name or reason (optional)", "")

    filtered_df = df[
        (df['timestamp'].dt.date >= start_date) &
        (df['timestamp'].dt.date <= end_date)
    ]

    if keyword:
        keyword_lower = keyword.lower()
        filtered_df = filtered_df[
            filtered_df['name'].str.lower().str.contains(keyword_lower) |
            filtered_df['reason'].str.lower().str.contains(keyword_lower)
        ]

    # Display table
    st.subheader("📋 Filtered Visitors")
    st.dataframe(filtered_df.sort_values("timestamp", ascending=False), use_container_width=True)

    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Filtered CSV", data=csv, file_name=f"{doctor}_filtered_visitors.csv", mime='text/csv')

    # Charts
    st.divider()
    st.subheader("📊 Visitor Analytics")

    # Number of visitors per day
    visits_per_day = filtered_df.groupby(filtered_df['timestamp'].dt.date).size().reset_index(name='count')
    if not visits_per_day.empty:
        st.plotly_chart(px.bar(visits_per_day, x='timestamp', y='count', title="Visitors Per Day"))

    # Number of visitors per hour
    visits_per_hour = filtered_df.groupby(filtered_df['timestamp'].dt.hour).size().reset_index(name='count')
    if not visits_per_hour.empty:
        st.plotly_chart(px.line(visits_per_hour, x='timestamp', y='count', markers=True, title="Visitors Per Hour"))

    # Number of visitors per reason
    visits_per_reason = filtered_df.groupby("reason").size().reset_index(name='count')
    if not visits_per_reason.empty:
        st.plotly_chart(px.pie(visits_per_reason, names="reason", values="count", title="Visitors by Reason"))
