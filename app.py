import streamlit as st

# Set the page configuration
st.set_page_config(page_title="Clinic Dashboard", layout="wide", initial_sidebar_state="expanded")

# Sidebar content
with st.sidebar:
    st.title("Clinic Navigation")
    st.markdown("Welcome to the clinic dashboard.")
    st.page_link("pages/visitors.py", label="Visitor Records")
    st.page_link("pages/analytics.py", label="Analytics")
    st.page_link("pages/settings.py", label="Settings")

# Main content
st.title("Welcome to the Clinic Dashboard")
st.write("Use the sidebar to navigate through the application.")
