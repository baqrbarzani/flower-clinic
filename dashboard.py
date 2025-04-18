import streamlit as st
import sqlite3
import pandas as pd

def get_db_connection():
    conn = sqlite3.connect("clinic.db", check_same_thread=False)
    return conn

def create_visitors_table():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            disease TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def show_dashboard():
    st.title("Visitor Dashboard")

    # Create table if not exists
    create_visitors_table()

    # Input form
    with st.form("visitor_form"):
        name = st.text_input("Visitor Name")
        disease = st.selectbox("Select Disease", [
            "Back Pain", "Neck Pain", "Frozen Shoulder", "Knee Osteoarthritis",
            "Ankylosing Spondylitis", "Stroke Rehabilitation", "Parkinson’s Disease",
            "Multiple Sclerosis", "Spinal Cord Injury", "Cerebral Palsy",
            "Pelvic Floor Dysfunction", "COPD", "Cystic Fibrosis",
            "Post-Surgical Rehabilitation", "Sports Injury", "Balance Disorders",
            "Gait Disorders", "Carpal Tunnel Syndrome", "Tendinitis", "Other"
        ])
        submitted = st.form_submit_button("Submit")

        if submitted:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("INSERT INTO visitors (name, disease) VALUES (?, ?)", (name, disease))
            conn.commit()
            conn.close()
            st.success("Visitor added successfully!")

    # Display saved records
    st.subheader("Visitor Records")
    try:
        conn = get_db_connection()
        df = pd.read_sql_query("SELECT * FROM visitors ORDER BY timestamp DESC", conn)
        st.dataframe(df)
        conn.close()
    except Exception as e:
        st.error("Error loading visitor data.")
        st.text(str(e))
