import sqlite3
import csv

def import_csv_to_db(csv_file_path):
    conn = sqlite3.connect('clinic_visitors.db')
    cursor = conn.cursor()

    # Create the tables if they don't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS diseases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS visitors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        visit_date TEXT NOT NULL,
        disease_id INTEGER,
        FOREIGN KEY (disease_id) REFERENCES diseases(id)
    )
    ''')

    # Read the CSV file and insert data
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Insert disease data
            cursor.execute('''
            INSERT OR IGNORE INTO diseases (name) VALUES (?)
            ''', (row['disease_name'],))

            # Get the disease_id
            cursor.execute('''
            SELECT id FROM diseases WHERE name = ?
            ''', (row['disease_name'],))
            disease_id = cursor.fetchone()[0]

            # Insert visitor data
            cursor.execute('''
            INSERT INTO visitors (name, visit_date, disease_id)
            VALUES (?, ?, ?)
            ''', (row['name'], row['visit_date'], disease_id))

    conn.commit()
    conn.close()
