import streamlit as st
from dashboard import show_dashboard
from PIL import Image

# Show image in sidebar (must be a valid path or URL)
st.sidebar.image("assets/health.jpg", use_column_width=True, caption="Flower Health Clinic")

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Dashboard"])

if page == "Dashboard":
    show_dashboard()
