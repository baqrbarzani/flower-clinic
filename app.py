import streamlit as st
import os
import pandas as pd
from database import initialize_database, import_csv_to_db
from login import show_login

# Initialize the database
initialize_database()

# Session state to manage authentication
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Display login or main app based on authentication
if not st.session_state['authenticated']:
    show_login()
else:
    st.title("Clinic Visitor Management")

    # File uploader for CSV
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
    if uploaded_file is not None:
        # Save uploaded file to a temporary location
        temp_path = os.path.join("temp_uploaded.csv")
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        try:
            import_csv_to_db(temp_path)
            st.success("CSV data imported successfully.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            os.remove(temp_path)

    # Display visitors data
    conn = sqlite3.connect('clinic_visitors.db')
    df = pd.read_sql_query('''
        SELECT visitors.id, visitors.name, visitors.visit_date, diseases.name as disease
        FROM visitors
        JOIN diseases ON visitors.disease_id = diseases.id
    ''', conn)
    conn.close()

    st.subheader("Visitor Records")
    st.dataframe(df)
