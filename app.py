import streamlit as st
from dashboard import show_dashboard
from sidebar import show_sidebar
from style import set_custom_style

st.set_page_config(page_title="Clinic Visitor Manager", layout="centered")

set_custom_style()  # Optional: for custom styles
show_sidebar()      # Doctor login and selection
show_dashboard()    # Main visitor interface
