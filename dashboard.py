# dashboard.py
import streamlit as st

def show_dashboard():
    st.title("Visitor Dashboard")

    # Input for visitor name
    visitor_name = st.text_input("Visitor Name")

    # List of diseases
    diseases = [
        "Back Pain", "Neck Pain", "Frozen Shoulder", "Knee Osteoarthritis",
        "Ankylosing Spondylitis", "Stroke Rehabilitation", "Parkinson’s Disease",
        "Multiple Sclerosis", "Spinal Cord Injury", "Cerebral Palsy",
        "Pelvic Floor Dysfunction", "COPD", "Cystic Fibrosis",
        "Post-Surgical Rehabilitation", "Sports Injury", "Balance Disorders",
        "Gait Disorders", "Carpal Tunnel Syndrome", "Tendinitis", "Other"
    ]

    # Dropdown to select disease
    selected_disease = st.selectbox("Select Disease", diseases)

    if st.button("Submit"):
        st.success(f"Visitor '{visitor_name}' recorded with disease: {selected_disease}")
