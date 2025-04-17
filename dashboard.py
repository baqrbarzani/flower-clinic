with st.form("visitor_form"):
    name = st.text_input("Visitor's Name")
    reason = st.selectbox(
        "Reason for Visit",
        [
            "Back Pain",
            "Neck Pain",
            "Frozen Shoulder",
            "Knee Osteoarthritis",
            "Ankylosing Spondylitis",
            "Stroke Rehabilitation",
            "Parkinson’s Disease",
            "Multiple Sclerosis",
            "Spinal Cord Injury",
            "Cerebral Palsy",
            "Pelvic Floor Dysfunction",
            "Chronic Obstructive Pulmonary Disease (COPD)",
            "Cystic Fibrosis",
            "Post-Surgical Rehabilitation",
            "Sports Injury",
            "Balance Disorders",
            "Gait Disorders",
            "Carpal Tunnel Syndrome",
            "Tendinitis",
            "Other"
        ]
    )
    submitted = st.form_submit_button("Add Visitor")

    if submitted:
        if name and reason:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute('''
                INSERT INTO visitors (doctor, name, reason, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (doctor, name, reason, timestamp))
            conn.commit()
            st.success("Visitor added successfully.")
        else:
            st.warning("Please fill in all fields.")
