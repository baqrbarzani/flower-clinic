import streamlit as st
from database import initialize_database
from login import show_login

initialize_database()

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    show_login()
else:
    # Your main app code here
    st.title("Welcome to the Clinic Visitor Management System")
