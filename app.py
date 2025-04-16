import streamlit as st
from dashboard import show_dashboard
from sidebar import show_sidebar
from style import set_custom_style

st.set_page_config(page_title="Clinic Visitor Manager", layout="centered")

set_custom_style()        # Optional custom style
show_sidebar()            # Show login sidebar
show_dashboard()          # Show main content if logged in
