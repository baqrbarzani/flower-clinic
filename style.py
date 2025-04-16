import streamlit as st

def set_custom_style():
    st.markdown("""
        <style>
        .stButton>button {
            border-radius: 10px;
            background-color: #1f77b4;
            color: white;
            padding: 6px 12px;
        }
        </style>
    """, unsafe_allow_html=True)
