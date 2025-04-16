import streamlit as st

st.set_page_config(page_title="Clinic Visitor Manager", layout="centered")

st.title("🏥 Clinic Visitor Management")

# Sample doctor list
doctors = ["Dr. Smith", "Dr. Johnson", "Dr. Patel", "Dr. Lee"]

# Initialize session state
if "visitor_data" not in st.session_state:
    st.session_state.visitor_data = {doc: [] for doc in doctors}

# Select doctor
selected_doctor = st.selectbox("Select a doctor to view or register visitors:", doctors)

st.subheader(f"Register a new visitor for {selected_doctor}")

with st.form(key="visitor_form"):
    name = st.text_input("Visitor's name")
    reason = st.text_area("Reason for visit")
    submit = st.form_submit_button("Add Visitor")

    if submit:
        if name and reason:
            st.session_state.visitor_data[selected_doctor].append({"name": name, "reason": reason})
            st.success(f"Visitor '{name}' added for {selected_doctor}")
        else:
            st.warning("Please fill in all fields.")

st.divider()

st.subheader(f"Visitors for {selected_doctor}")

visitors = st.session_state.visitor_data[selected_doctor]

if visitors:
    for v in visitors:
        st.write(f"- **{v['name']}**: {v['reason']}")
else:
    st.info("No visitors registered yet.")

