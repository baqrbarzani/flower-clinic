import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import plotly.express as px

def show_dashboard():
    if not st.session_state.get("logged_in"):
        st.info("Please log in to continue.")
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

    c.execute('''
        CREATE TABLE IF NOT EXISTS diseases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')
    conn.commit()

    st.header("📝 New Visitor Entry")

    # Get disease options from DB
    c.execute("SELECT name FROM diseases ORDER BY name")
    disease_options = [row[0] for row in c.fetchall()]
    disease_options.append("Other")

    with st.form("visitor_form"):
        name = st.text_input("Visitor's Name")
        reason = st.selectbox("Reason for Visit", disease_options)
        if reason == "Other":
            custom_reason = st.text_input("Enter custom reason")
            reason = custom_reason

        if st.form_submit_button("Add Visitor"):
            if name and reason:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute("INSERT INTO visitors (doctor, name, reason, timestamp) VALUES (?, ?, ?, ?)", 
                          (doctor, name, reason, timestamp))
                conn.commit()
                st.success("Visitor added!")
            else:
                st.warning("All fields are required.")

    st.divider()
    st.subheader("🗃 Manage Diseases")

    tab1, tab2 = st.tabs(["➕ Add Disease", "🧾 Edit Diseases"])

    with tab1:
        new_disease = st.text_input("Disease Name")
        if st.button("Add Disease"):
            if new_disease.strip():
                try:
                    c.execute("INSERT INTO diseases (name) VALUES (?)", (new_disease.strip(),))
                    conn.commit()
                    st.success("Disease added.")
                except sqlite3.IntegrityError:
                    st.warning("Disease already exists.")

    with tab2:
        c.execute("SELECT * FROM diseases ORDER BY name")
        diseases = c.fetchall()
        for disease_id, name in diseases:
            col1, col2, col3 = st.columns([3, 1, 1])
            new_name = col1.text_input(f"Edit {disease_id}", value=name, key=f"name_{disease_id}")
            if col2.button("Update", key=f"upd_{disease_id}"):
                c.execute("UPDATE diseases SET name = ? WHERE id = ?", (new_name, disease_id))
                conn.commit()
                st.success("Updated.")
            if col3.button("Delete", key=f"del_{disease_id}"):
                c.execute("DELETE FROM diseases WHERE id = ?", (disease_id,))
                conn.commit()
                st.success("Deleted.")
                st.experimental_rerun()

    # Filter visitor data
    df = pd.read_sql_query("SELECT name, reason, timestamp FROM visitors WHERE doctor = ?", conn, params=(doctor,))
    if df.empty:
        st.info("No visitors yet.")
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    st.divider()
    st.subheader("🔎 Visitor History & Charts")

    col1, col2 = st.columns(2)
    start_date = col1.date_input("Start Date", df["timestamp"].min().date())
    end_date = col2.date_input("End Date", df["timestamp"].max().date())
    keyword = st.text_input("Search by name or reason")

    filtered_df = df[
        (df["timestamp"].dt.date >= start_date) &
        (df["timestamp"].dt.date <= end_date)
    ]
    if keyword:
        keyword = keyword.lower()
        filtered_df = filtered_df[
            filtered_df["name"].str.lower().str.contains(keyword) |
            filtered_df["reason"].str.lower().str.contains(keyword)
        ]

    st.dataframe(filtered_df.sort_values("timestamp", ascending=False), use_container_width=True)

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download CSV", data=csv, file_name=f"{doctor}_visitors.csv", mime="text/csv")

    st.divider()
    st.subheader("📊 Visitor Charts")

    daily_visits = filtered_df.groupby(filtered_df["timestamp"].dt.date).size().reset_index(name="count")
    if not daily_visits.empty:
        st.plotly_chart(px.bar(daily_visits, x="timestamp", y="count", title="Visitors per Day"))

    by_reason = filtered_df["reason"].value_counts().reset_index()
    by_reason.columns = ["reason", "count"]
    if not by_reason.empty:
        st.plotly_chart(px.pie(by_reason, names="reason", values="count", title="Reasons for Visits"))

    by_hour = filtered_df.groupby(filtered_df["timestamp"].dt.hour).size().reset_index(name="count")
    if not by_hour.empty:
        st.plotly_chart(px.line(by_hour, x="timestamp", y="count", title="Visitors by Hour", markers=True))
