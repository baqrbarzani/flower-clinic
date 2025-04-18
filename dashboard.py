import streamlit as st
from database import get_db_connection

def show_dashboard():
    st.subheader("Dashboard")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT disease_name FROM diseases")
    diseases = cursor.fetchall()
    conn.close()
    st.write("List of Diseases:")
    for disease in diseases:
        st.write(f"- {disease['disease_name']}")
