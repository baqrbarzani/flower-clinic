import sqlite3
import csv
import os

DB_NAME = 'clinic_visitors.db'

def initialize_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
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
    conn.commit()
    conn.close()

def verify_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def import_csv_to_db(csv_file_path):
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"CSV file not found at path: {csv_file_path}")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            disease_name = row.get('disease_name')
            visitor_name = row.get('name')
            visit_date = row.get('visit_date')

            if not (disease_name and visitor_name and visit_date):
                continue  # Skip rows with missing data

            cursor.execute('INSERT OR IGNORE INTO diseases (name) VALUES (?)', (disease_name,))
            cursor.execute('SELECT id FROM diseases WHERE name = ?', (disease_name,))
            disease_id = cursor.fetchone()[0]

            cursor.execute('''
                INSERT INTO visitors (name, visit_date, disease_id)
                VALUES (?, ?, ?)
            ''', (visitor_name, visit_date, disease_id))

    conn.commit()
    conn.close()
