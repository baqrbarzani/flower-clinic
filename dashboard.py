import streamlit as st
from database import get_db_connection

def show_dashboard():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.warning("Please log in to access the dashboard.")
        return

    st.title(f"Welcome to the Dashboard, Dr. {st.session_state.username}")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT disease_name FROM diseases")
    diseases = cursor.fetchall()
    conn.close()

    if diseases:
        st.write("List of Diseases:")
        for disease in diseases:
            st.write(f"- {disease['disease_name']}")
    else:
        st.write("No diseases found.")
