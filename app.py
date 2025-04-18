import streamlit as st
from database import initialize_database, import_csv_to_db
import os

# Initialize the database
initialize_database()

# Import CSV data into the database
csv_file_path = os.path.join(os.path.dirname(__file__), 'your_data.csv')
import_csv_to_db(csv_file_path)

# Your Streamlit app code continues here...
