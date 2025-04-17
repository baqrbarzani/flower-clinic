import streamlit as st

# Dummy credentials for doctors
DOCTOR_CREDENTIALS = {
    "dr_ali": "1234",
    "dr_lina": "5678"
}

def show_login():
    st.title("🔐 Doctor Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")

        if login_btn:
            if username in DOCTOR_CREDENTIALS and DOCTOR_CREDENTIALS[username] == password:
                st.session_state.logged_in = True
                st.session_state.doctor = username
                st.success("Logged in successfully.")
                st.experimental_set_query_params(page="dashboard")
                st.stop()  # <- instead of rerun, just stop here
            else:
                st.error("Invalid credentials.")
