import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from database import initialize_database
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
    st.title("Clinic Visitor Management Dashboard")

    # Connect to the database
    conn = sqlite3.connect('clinic_visitors.db')
    cursor = conn.cursor()

    # Fetch data
    cursor.execute('''
        SELECT visitors.id, visitors.name, visitors.visit_date, diseases.name as disease
        FROM visitors
        JOIN diseases ON visitors.disease_id = diseases.id
    ''')
    data = cursor.fetchall()
    conn.close()

    # Create DataFrame
    df = pd.DataFrame(data, columns=['ID', 'Name', 'Visit Date', 'Disease'])

    # Display KPIs
    total_visitors = df['ID'].nunique()
    unique_diseases = df['Disease'].nunique()

    col1, col2 = st.columns(2)
    col1.metric("Total Visitors", total_visitors)
    col2.metric("Unique Diseases", unique_diseases)

    # Display data table
    st.subheader("Visitor Records")
    st.dataframe(df)

    # Plot: Visits per Disease
    st.subheader("Visits per Disease")
    disease_counts = df['Disease'].value_counts()
    fig, ax = plt.subplots()
    disease_counts.plot(kind='bar', ax=ax)
    ax.set_xlabel("Disease")
    ax.set_ylabel("Number of Visits")
    st.pyplot(fig)
