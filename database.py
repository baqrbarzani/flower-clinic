import sqlite3
import os
import csv

DB_PATH = os.path.join(os.path.dirname(__file__), "clinic_visitors.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS diseases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease_name TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            visit_date TEXT NOT NULL,
            disease_id INTEGER,
            FOREIGN KEY (disease_id) REFERENCES diseases(id)
        )
    """)

    conn.commit()
    conn.close()

def import_csv_to_db(csv_file_path):
    conn = get_db_connection()
    cursor = conn.cursor()

    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
                INSERT OR REPLACE INTO diseases (disease_name)
                VALUES (?)
            """, (row['disease_name'],))

            cursor.execute("""
                INSERT INTO visitors (name, visit_date, disease_id)
                VALUES (?, ?, ?)
            """, (row['name'], row['visit_date'], row['disease_id']))

    conn.commit()
    conn.close()
