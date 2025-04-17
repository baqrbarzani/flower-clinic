import sqlite3
import os

# Define the path to the database file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "clinic_visitors.db")

def initialize_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Create the 'diseases' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diseases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease_name TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

# Call the function to initialize the database
initialize_database()
