import streamlit as st
from dashboard import show_dashboard
from login import show_login
from sidebar import show_sidebar
from style import set_custom_style

# Set Streamlit page configuration
st.set_page_config(page_title="Clinic Visitor Manager", layout="centered")

# Set custom styling
set_custom_style()

# Display sidebar
show_sidebar()

# Display content based on the page selection
page = st.sidebar.radio("Navigation", ["Login", "Dashboard"])

if page == "Login":
    show_login()
elif page == "Dashboard":
    show_dashboard()
