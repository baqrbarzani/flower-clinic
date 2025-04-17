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

    # Create necessary tables
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

    st.header("📝 Register a New Visitor")

    # Load diseases from DB
    c.execute("SELECT name FROM diseases ORDER BY name")
    disease_options = [row[0] for row in c.fetchall()]
    disease_options.append("Other")

    with st.form("visitor_form"):
        name = st.text_input("Visitor's Name")
        reason = st.selectbox("Reason for Visit", disease_options)

        if reason == "Other":
            custom_reason = st.text_input("Please specify the reason")
            reason_to_save = custom_reason
        else:
            reason_to_save = reason

        submitted = st.form_submit_button("Add Visitor")

        if submitted:
            if name and reason_to_save:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute('''
                    INSERT INTO visitors (doctor, name, reason, timestamp)
                    VALUES (?, ?, ?, ?)
                ''', (doctor, name, reason_to_save, timestamp))
                conn.commit()
                st.success("Visitor added successfully.")
            else:
                st.warning("Please fill in all fields.")

    st.divider()
    st.subheader("🛠 Manage Diseases")

    tab1, tab2 = st.tabs(["➕ Add Disease", "🗂 View & Edit Diseases"])

    with tab1:
        new_disease = st.text_input("New Disease Name")
        if st.button("Add Disease"):
            if new_disease.strip():
                try:
                    c.execute("INSERT INTO diseases (name) VALUES (?)", (new_disease.strip(),))
                    conn.commit()
                    st.success(f"{new_disease} added.")
                except sqlite3.IntegrityError:
                    st.warning("This disease already exists.")
            else:
                st.warning("Please enter a valid name.")

    with tab2:
        c.execute("SELECT * FROM diseases ORDER BY name")
        diseases = c.fetchall()
        for disease_id, name in diseases:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                updated_name = st.text_input(f"Edit {disease_id}", value=name, key=f"edit_{disease_id}")
            with col2:
                if st.button("Update", key=f"update_{disease_id}"):
                    c.execute("UPDATE diseases SET name = ? WHERE id = ?", (updated_name, disease_id))
                    conn.commit()
                    st.success("Updated.")
            with col3:
                if st.button("Delete", key=f"delete_{disease_id}"):
                    c.execute("DELETE FROM diseases WHERE id = ?", (disease_id,))
                    conn.commit()
                    st.success("Deleted.")
                    st.experimental_rerun()

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

    # Visitors per day
    visits_per_day = filtered_df.groupby(filtered_df['timestamp'].dt.date).size().reset_index(name='count')
    if not visits_per_day.empty:
        fig1 = px.bar(visits_per_day, x='timestamp', y='count', title="Visitors Per Day", labels={'timestamp': 'Date', 'count': 'Number of Visitors'})
        st.plotly_chart(fig1, use_container_width=True)

    # Visitors per hour
    visits_per_hour = filtered_df.groupby(filtered_df['timestamp'].dt.hour).size().reset_index(name='count')
    if not visits_per_hour.empty:
        fig2 = px.line(visits_per_hour, x='timestamp', y='count', markers=True, title="Visitors Per Hour", labels={'timestamp': 'Hour', 'count': 'Number of Visitors'})
        st.plotly_chart(fig2, use_container_width=True)

    # Visitors by reason
    visits_by_reason = filtered_df['reason'].value_counts().reset_index()
    visits_by_reason.columns = ['reason', 'count']
    if not visits_by_reason.empty:
        fig3 = px.pie(visits_by_reason, names='reason', values='count', title="Visitors by Reason")
        st.plotly_chart(fig3, use_container_width=True)
