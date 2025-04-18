import sqlite3
import csv

def import_csv_to_db(csv_file_path):
    conn = sqlite3.connect('clinic_visitors.db')
    cursor = conn.cursor()

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("""
                INSERT OR REPLACE INTO diseases (disease_name)
                VALUES (?)
            """, (row['disease_name'],))

            cursor.execute("""
                INSERT INTO visitors (name, visit_date, disease_id)
                VALUES (?, ?, (SELECT id FROM diseases WHERE disease_name = ?))
            """, (row['name'], row['visit_date'], row['disease_name']))

    conn.commit()
    conn.close()
