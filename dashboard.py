import streamlit as st
import sqlite3

# Initialize disease table if not already created
def init_disease_db():
    conn = sqlite3.connect("clinic_visitors.db", check_same_thread=False)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS diseases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease_name TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

# Function to add a disease to the database
def add_disease(disease_name):
    conn = sqlite3.connect("clinic_visitors.db", check_same_thread=False)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO diseases (disease_name) VALUES (?)", (disease_name,))
        conn.commit()
    except sqlite3.IntegrityError:
        st.warning(f"{disease_name} already exists in the database.")
    finally:
        conn.close()

# Function to fetch all diseases from the database
def get_diseases():
    conn = sqlite3.connect("clinic_visitors.db", check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT disease_name FROM diseases")
    diseases = c.fetchall()
    conn.close()
    return [d[0] for d in diseases]

def show_dashboard():
    init_disease_db()  # Initialize the database for diseases

    st.title("Clinic Dashboard")
    
    # Add a disease form
    st.subheader("Add a New Disease")
    new_disease = st.text_input("Enter the name of the disease")

    if st.button("Add Disease"):
        if new_disease:
            add_disease(new_disease)
            st.success(f"Added '{new_disease}' to the list of diseases.")
            st.experimental_rerun()  # Refresh the page to show updated list
        else:
            st.warning("Please enter a disease name.")

    # Display the list of existing diseases
    st.subheader("Diseases List")
    diseases = get_diseases()

    if diseases:
        for disease in diseases:
            st.write(f"- {disease}")
    else:
        st.write("No diseases found.")
