import streamlit as st

def show_sidebar():
    st.sidebar.title("🔐 Doctor Login")

    doctor_credentials = {
        "Dr. Smith": "smith123",
        "Dr. Johnson": "johnson123",
        "Dr. Patel": "patel123",
        "Dr. Lee": "lee123"
    }

    if not st.session_state.get("logged_in"):
        with st.sidebar.form("login_form"):
            doctor_name = st.selectbox("Select your name", list(doctor_credentials.keys()))
            password = st.text_input("Enter password", type="password")
            login_btn = st.form_submit_button("Login")

        if login_btn:
            if password == doctor_credentials.get(doctor_name):
                st.session_state.logged_in = True
                st.session_state.doctor = doctor_name
                st.success(f"Welcome, {doctor_name}")
            else:
                st.error("Incorrect password.")
    else:
        st.sidebar.success(f"Logged in as {st.session_state.doctor}")
        if st.sidebar.button("🔓 Logout"):
            st.session_state.logged_in = False
            st.session_state.doctor = None
            st.experimental_rerun()
