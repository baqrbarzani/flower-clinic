import streamlit as st
from dashboard import show_dashboard
from login import show_login
from database import initialize_database

# Initialize database
initialize_database()

# Sidebar navigation
st.sidebar.title("Flower Health Clinic")
page = st.sidebar.selectbox("Go to", ["Login", "Dashboard"])

# Page routing
if page == "Login":
    show_login()
elif page == "Dashboard":
    show_dashboard()
