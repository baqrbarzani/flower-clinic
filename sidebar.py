import streamlit as st

def show_sidebar():
    st.sidebar.title("🔐 Doctor Login")

    # Display doctor selection if not logged in
    if not st.session_state.get("logged_in"):
        st.sidebar.markdown("### Login to Access the Dashboard")
    else:
        st.sidebar.success(f"Logged in as {st.session_state.doctor}")
